from http import HTTPStatus

from api.pagination import RecipePagination, UserPagination
from api.permissions import CustomIsAuthenticated
from api.serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeReadSerializer,
    RecipeShopCartSerializer,
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
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
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
            {"detail": "Пароль успешно изменен!"},
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
        searilizer = SubscribeSerializer(
            page,
            many=True,
            context={"user": request.user},
        )
        return Response(searilizer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=(CustomIsAuthenticated,),
    )
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(CustomUser, id=kwargs["pk"])
        user = request.user

        if request.method == "POST":
            if user == author:
                return Response(
                    {"errors": "Вы не можете подписаться на самого себя"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if Subscribe.objects.filter(user=user, author=author).exists():
                return Response(
                    {"errors": "Вы уже подписаны на данного пользователя"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = SubscribeSerializer(
                author,
                data=request.data,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(user=request.user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            if user == author:
                return Response(
                    {"errors": "Вы не можете отписываться от самого себя"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            get_object_or_404(Subscribe, user=request.user, author=author).delete()
            return Response(
                {"detail": "Подписка отменена!"},
                status=status.HTTP_204_NO_CONTENT,
            )


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
                "Изменение чужого контента запрещено!",
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
            serializer = RecipeShopCartSerializer(
                recipe, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            if not ShopCart.objects.filter(user=request.user, recipe=recipe).exists():
                ShopCart.objects.create(user=request.user, recipe=recipe)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {"errors": "Рецепт уже есть в списке покупок!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.method == "DELETE":
            get_object_or_404(ShopCart, user=request.user, recipe=recipe).delete()
            return Response(
                {"detail": "Рецепт удален из списка покупок в корзине!"},
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
            serializer = RecipeShopCartSerializer(
                recipe, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            if not Favorite.objects.filter(user=request.user, recipe=recipe).exists():
                Favorite.objects.create(user=request.user, recipe=recipe)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {"errors": "Рецепт уже есть в списке избранных!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.method == "DELETE":
            get_object_or_404(Favorite, user=request.user, recipe=recipe).delete()
            return Response(
                {"detail": "Рецепт удален из списка избранных!"},
                status=status.HTTP_204_NO_CONTENT,
            )

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[CustomIsAuthenticated],
        pagination_class=None,
    )
    def download_shopping_cart(self, request, **kwargs):
        carts = ShopCart.objects.filter(user=self.request.user)
        recipe_id = [cart.recipe.id for cart in carts]
        ingredients = (
            Recipe_ingredient.objects.filter(recipe__in=recipe_id)
            .values("ingredient")
            .annotate(amount=Sum("amount"))
            .values_list("ingredient__name", "ingredient__measurement_unit", "amount")
        )
        list_shop = ""
        for ingredient in ingredients:
            list_shop += f"{ingredient[0]} ({ingredient[1]}) - {ingredient[2]}\n"
        response = HttpResponse(list_shop, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename=shopping-list.txt"
        return response


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
