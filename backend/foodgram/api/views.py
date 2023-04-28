from api.pagination import RecipePagination, UserPagination
from api.permissions import CustomIsAuthenticated
from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
    UserCreateSerializer,
    UserReadSerializer,
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
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, mixins, permissions, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from users.models import CustomUser


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Пользователи"""

    queryset = CustomUser.objects.all()
    serializer_class = UserReadSerializer
    pagination_class = UserPagination

    def get_serialize_class(self):
        if self.action in ("list", "retrive"):
            return UserReadSerializer
        return UserCreateSerializer

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[CustomIsAuthenticated],
    )
    def me(self, request):
        pass


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
