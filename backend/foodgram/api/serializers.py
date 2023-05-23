from django.contrib.auth.password_validation import validate_password

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from app.models import CustomUser, Ingredient, Recipe, Recipe_ingredient, Subscribe, Tag

MESSAGE_OVERLAP_PASS = "Пароль не должен совпадать с текущим!"
MESSAGE_INCORRECT_PASS = "Не корректный пароль"
MESSAGE_MIN_ELEMENT = "Необходиом ввести не менее одного элемента"


class UserReadSerializer(serializers.ModelSerializer):
    """[GET] Список пользователей"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        if self.context.get("request") and not self.context["request"].user.is_anonymous:
            user = self.context["request"].user
            return user.subscriber.filter(author=obj).exists()
        return False


class UserCreateSerializer(serializers.ModelSerializer):
    """[POST] Создание нового пользователя."""

    class Meta:
        model = CustomUser
        fields = ("email", "username", "first_name", "last_name", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class ResetPasswordSerialize(serializers.ModelSerializer):
    """[POST] Изменение пароля пользователя."""

    new_password = serializers.CharField()
    current_password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ("new_password", "current_password")

    def validate(self, data):
        if data["new_password"] == data["current_password"]:
            raise serializers.ValidationError(MESSAGE_OVERLAP_PASS)
        if validate_password(data["new_password"]):
            raise serializers.ValidationError(MESSAGE_INCORRECT_PASS)
        return data

    def update(self, instance, validated_data):
        if instance.check_password(validated_data.get("current_password")):
            instance.set_password(validated_data["new_password"])
            instance.save()
        else:
            raise serializers.ValidationError(MESSAGE_INCORRECT_PASS)
        return instance


class TagSerializer(serializers.ModelSerializer):
    """[GET] Список тегов"""

    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    """Список индигринетов"""

    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "measurement_unit",
        )


class RecipeCreadIngredientSerializer(serializers.ModelSerializer):
    """Список ингредиентов"""

    id = serializers.ReadOnlyField(source="ingredient.id")
    amount = serializers.IntegerField()

    class Meta:
        model = Recipe_ingredient
        fields = (
            "id",
            "amount",
        )


class RecipeReadIngredientSerializer(serializers.ModelSerializer):
    """Список ингредиентов"""

    id = serializers.ReadOnlyField(source="ingredient.id")
    amount = serializers.IntegerField()
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(source="ingredient.measurement_unit")

    class Meta:
        model = Recipe_ingredient
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class RecipeReadSerializer(serializers.ModelSerializer):
    """[GET] получение рецептов"""

    image = Base64ImageField(read_only=True)
    ingredients = RecipeReadIngredientSerializer(
        many=True,
        source="recipe_ingredient",
    )
    author = UserReadSerializer()
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "author",
            "tags",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        if self.context.get("request") and not self.context["request"].user.is_anonymous:
            user = self.context["request"].user
            return user.favorite_user.filter(recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        if self.context.get("request") and not self.context["request"].user.is_anonymous:
            user = self.context["request"].user
            return user.carts.filter(recipe=obj).exists()
        return False


class RecipeCreateSerializer(serializers.ModelSerializer):
    """[POST, PATCH, DELETE] создание, правка и удаление рецептов"""

    image = Base64ImageField()
    ingredients = RecipeCreadIngredientSerializer(
        many=True,
        read_only=True,
        source="recipe_ingredient",
    )

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags_data = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            Recipe_ingredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get("id"),
                amount=ingredient.get("amount"),
            )
        recipe.tags.set(tags_data)
        return recipe

    def validate(self, data):
        ingredients = self.initial_data.get("ingredients")
        if not ingredients or len(ingredients) < 1:
            raise serializers.ValidationError(MESSAGE_MIN_ELEMENT)
        for ingredient in ingredients:
            if int(ingredient["amount"]) <= 0:
                ingredient_set = Ingredient.objects.get(pk=ingredient["id"])
                raise serializers.ValidationError(
                    f"Проверте ингредиент '{ingredient_set.name}', количество должно превышать 0"
                )
        data["ingredients"] = ingredients
        return data

    def update(self, instance, validated_data):
        instance.image = validated_data.get("image", instance.image)
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time",
            instance.cooking_time,
        )
        tags = validated_data.pop("tags")
        instance.tags.set(tags)
        ingredients = validated_data.pop("ingredients")
        Recipe_ingredient.objects.filter(
            recipe=instance,
            ingredient__in=instance.ingredients.all(),
        ).delete()
        Recipe_ingredient.objects.bulk_create(
            [
                Recipe_ingredient(
                    recipe=instance,
                    ingredient=Ingredient.objects.get(pk=ingredient["id"]),
                    amount=ingredient["amount"],
                )
                for ingredient in ingredients
            ]
        )
        instance.save()
        return instance

    class Meta:
        model = Recipe
        fields = (
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        )


class RecipeShopCartSerializer(serializers.ModelSerializer):
    """Рецепт в корзине покупок"""

    image = Base64ImageField(required=False, allow_null=True)
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class SubscribeSerializer(serializers.ModelSerializer):
    """[GET] Список авторов на которых подписан пользователь"""

    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        is_subscribed = Subscribe.objects.filter(author=obj, user=self.context["request"].user).exists()
        return is_subscribed

    def get_recipes(self, obj):
        request = self.context.get("request")
        limit = request.GET.get("recipes_limit")
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[: int(limit)]
        serializer = RecipeShopCartSerializer(recipes, many=True, read_only=True)
        return serializer.data
