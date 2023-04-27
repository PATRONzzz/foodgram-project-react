import base64
from ast import Import
from dataclasses import field

from api.pagination import UserPagination
from app.models import CustomUser, Ingredient, Recipe, ShopCard, Tag
from django.core.files.base import ContentFile
from rest_framework import permissions, serializers

# class Base64ImageField(serializers.ImageField):
#     def to_internal_value(self, data):
#         if isinstance(data, str) and data.startswith('data:image'):
#             format, imgstr = data.split(';base64,')
#             ext = format.split('/')[-1]
#             data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

#         return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    """[GET] Список пользователей"""

    class Meta:
        model = CustomUser
        fields = ("email", "id", "username", "first_name", "last_name", "password")


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
