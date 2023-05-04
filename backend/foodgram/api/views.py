from api.pagination import RecipePagination, UserPagination
from api.permissions import CustomIsAuthenticated
from api.serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeReadSerializer,
    ResetPasswordSerialize,
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
from rest_framework import filters, generics, mixins, permissions, status, viewsets
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
    pagination_class = UserPagination

    def get_serializer_class(self):
        if self.action in ("list", "retrive"):
            return UserReadSerializer
        return UserCreateSerializer

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[CustomIsAuthenticated],
    )
    def me(self, request):
        user = request.user
        serializer = UserReadSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(CustomIsAuthenticated,),
    )
    def set_password(self, request):
        serializer = ResetPasswordSerialize(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(
            {"detail": "The password is successfully changed!"},
            status=status.HTTP_204_NO_CONTENT,
        )


class RecipeViewSet(viewsets.ModelViewSet):
    """Рецепты"""

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeReadSerializer
        return RecipeCreateSerializer

    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    pagination_class = RecipePagination

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)

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

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("^name",)
