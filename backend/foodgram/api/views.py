from http import HTTPStatus

from api.pagination import RecipePagination, UserPagination
from api.permissions import CustomIsAuthenticated
from api.serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeReadSerializer,
    RecipeShopCardSerializer,
    ResetPasswordSerialize,
    SubscribeSerializer,
    TagSerializer,
    UserCreateSerializer,
    UserReadSerializer,
)
from app.models import (
    Favorite,
    Ingredient,
    Recipe,
    Recipe_ingredient,
    ShopCart,
    Subscribe,
    Tag,
)
from django.core.exceptions import PermissionDenied
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

    @action(
        detail=False,
        methods=[
            "get",
        ],
        permission_classes=(CustomIsAuthenticated,),
    )
    def subscriptions(self, request, **kwargs):
        queryset = CustomUser.objects.filter(autors__user=request.user)
        page = self.paginate_queryset(queryset)
        searilizer = SubscribeSerializer(page, many=True)
        return Response(searilizer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post", "delete"],
        permission_classes=(CustomIsAuthenticated,),
    )
    def subscribe(self, request, **kwargs):
        # recipe = get_object_or_404(Recipe, id=kwargs["pk"])
        # if request.method == "POST":
        #     serializer = RecipeShopCardSerializer(
        #         recipe, data=request.data, context={"request": request}
        #     )
        #     serializer.is_valid(raise_exception=True)
        #     if not ShopCart.objects.filter(user=request.user, recipe=recipe).exists():
        #         ShopCart.objects.create(user=request.user, recipe=recipe)
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     return Response(
        #         {"errors": "The recipe is already on the purchase list!"},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )
        # if request.method == "DELETE":
        #     get_object_or_404(ShopCart, user=request.user, recipe=recipe).delete()
        #     return Response(
        #         {"detail": "Recipe removed from shopp cart list!"},
        #         status=status.HTTP_204_NO_CONTENT,
        #     )
        return Response("Запрос получен")


class RecipeViewSet(viewsets.ModelViewSet):
    """Рецепты"""

    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    pagination_class = RecipePagination

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                "Changing someone else's content is prohibited!",
                HTTPStatus.FORBIDDEN,
            )
        super(RecipeViewSet, self).perform_update(serializer)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=(CustomIsAuthenticated,),
        pagination_class=None,
    )
    def shopping_cart(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs["pk"])
        if request.method == "POST":
            serializer = RecipeShopCardSerializer(
                recipe, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            if not ShopCart.objects.filter(user=request.user, recipe=recipe).exists():
                ShopCart.objects.create(user=request.user, recipe=recipe)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {"errors": "The recipe is already on the purchase list!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.method == "DELETE":
            get_object_or_404(ShopCart, user=request.user, recipe=recipe).delete()
            return Response(
                {"detail": "Recipe removed from shopp cart list!"},
                status=status.HTTP_204_NO_CONTENT,
            )

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=(CustomIsAuthenticated,),
        pagination_class=None,
    )
    def favorite(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs["pk"])
        if request.method == "POST":
            serializer = RecipeShopCardSerializer(
                recipe, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            if not Favorite.objects.filter(user=request.user, recipe=recipe).exists():
                Favorite.objects.create(user=request.user, recipe=recipe)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {"errors": "The recipe is already in the favorites list!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.method == "DELETE":
            get_object_or_404(Favorite, user=request.user, recipe=recipe).delete()
            return Response(
                {"detail": "Recipe removed from favorites list!"},
                status=status.HTTP_204_NO_CONTENT,
            )

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[CustomIsAuthenticated],
        pagination_class=None,
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
