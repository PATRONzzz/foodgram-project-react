import base64

import webcolors
from app.models import (CustomUser, Ingredient, Recipe, Recipe_ingredient,
                        ShopCart, Subscribe, Tag)
from django.contrib.auth.password_validation import validate_password
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import permissions, serializers


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError("There is no name for this color")
        return data


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


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
        if (self.context.get('request')
            and not self.context['request'].user.is_anonymous):
            return Subscribe.objects.filter(user=self.context['request'].user,
                                            author=obj).exists()
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
            raise serializers.ValidationError(
                "Пароль не должен совпадать с текущим!"
            )
        if validate_password(data["new_password"]):
            raise serializers.ValidationError("Не коректный пароль!")
        return data

    def update(self, instance, validated_data):
        if instance.check_password(validated_data.get("current_password")):
            instance.set_password(validated_data["new_password"])
            instance.save()
        else:
            raise serializers.ValidationError("Не верно введен текущий пароль")
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


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Список ингредиентов"""

    id = serializers.ReadOnlyField(source="ingredient.id")
    amount = serializers.IntegerField()

    class Meta:
        model = Recipe_ingredient
        fields = (
            "id",
            "amount",
        )


class RecipeReadSerializer(serializers.ModelSerializer):
    """[GET] получение рецептов"""

    image = Base64ImageField(required=False, allow_null=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        source="recipe_ingredient",
    )
    author = UserReadSerializer()
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()


    class Meta:
        model = Recipe
        fields = (
            "id",
            "author",
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        )
        
    # def get_is_favorited(self, obj):
    #     pass
    
    # def get_is_in_shopping_cart(self, obj):
    #     pass


class RecipeCreateSerializer(serializers.ModelSerializer):
    """[POST, PATCH, DELETE] создание, правка и удаление рецептов"""

    image = Base64ImageField(required=False, allow_null=True)
    ingredients = RecipeIngredientSerializer(
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
            raise serializers.ValidationError(
                "Необходимо ввести не менее одного ингредиента!"
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
        is_subscribed = Subscribe.objects.filter(
            author=obj, user=self.context['request'].user
        ).exists()
        return is_subscribed

    def get_recipes(self, obj):
        request = self.context.get("request")
        limit = request.GET.get("recipes_limit")
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[: int(limit)]
        serializer = RecipeShopCartSerializer(recipes, many=True, read_only=True)
        return serializer.data
