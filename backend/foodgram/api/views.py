from api.pagination import UserPagination
from api.permissions import CustomIsAuthenticated
from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
    UserSerializer,
)
from app.models import (
    Favorite,
    Ingredient,
    Recipe,
    Recipe_ingredient,
    ShopCard,
    Subscribe,
    Tag,
)
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from users.models import CustomUser


class UserViewSet(viewsets.ModelViewSet):
    """Пользователи"""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination


class RecipeViewSet(viewsets.ModelViewSet):
    """Рецепты"""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[CustomIsAuthenticated],
    )
    def download_shopping_cart(self, request):
        return Response("Запрос получен")


class TagViewSet(viewsets.ModelViewSet):
    """Теги"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """Ингридиенты"""

    queryset = Ingredient.objects
    serializer_class = IngredientSerializer
