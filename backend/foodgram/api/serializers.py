import base64
from ast import Import
from dataclasses import field

from app.models import CustomUser, Ingredient, Recipe, ShopCard, Tag
from django.contrib.auth.password_validation import validate_password
from django.core.files.base import ContentFile
from rest_framework import permissions, serializers

# class Base64ImageField(serializers.ImageField):
#     def to_internal_value(self, data):
#         if isinstance(data, str) and data.startswith('data:image'):
#             format, imgstr = data.split(';base64,')
#             ext = format.split('/')[-1]
#             data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

#         return super().to_internal_value(data)


class UserReadSerializer(serializers.ModelSerializer):
    """[GET] Список пользователей"""

    class Meta:
        model = CustomUser
        fields = ("email", "id", "username", "first_name", "last_name", "password")


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
                "The password should not match the current"
            )
        if validate_password(data["new_password"]):
            raise serializers.ValidationError("Incorrect password")
        return data

    def update(self, instance, validated_data):
        if instance.check_password(validated_data.get("current_password")):
            instance.set_password(validated_data["new_password"])
            instance.save()
        else:
            raise serializers.ValidationError("Current password is not correct")
        return instance


class TagSerializer(serializers.ModelSerializer):
    """[GET] Список тегов"""

    class Meta:
        model = Tag
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    """[GET] Список рецептов"""

    class Meta:
        model = Recipe
        fields = "__all__"


class ShopCardSerializer(serializers.ModelSerializer):
    """[GET] Список покупок"""

    class Meta:
        model = ShopCard
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    """Список индигринетов"""

    model = Ingredient
    fields = "__all__"
