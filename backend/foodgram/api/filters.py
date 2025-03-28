from django_filters import rest_framework as filters

from app.models import Recipe, Tag


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.BooleanFilter(method="is_favorited_filter")
    is_in_shopping_cart = filters.BooleanFilter(method="is_in_shopping_cart_filter")

    class Meta:
        model = Recipe
        fields = (
            "tags",
            "author",
        )

    def is_in_shopping_cart_filter(self, queryset, name, value):
        user = self.request.user
        if value == 1 and user.is_authenticated:
            return queryset.filter(shopcart_recipe__user=user)
        if value == 0 and user.is_authenticated:
            return queryset.exclude(shopcart_recipe__user=user)
        return queryset

    def is_favorited_filter(self, queryset, name, value):
        user = self.request.user
        if value == 1 and user.is_authenticated:
            return queryset.filter(favorite_recipe__user=user)
        if value == 0 and user.is_authenticated:
            return queryset.exclude(favorite_recipe__user=user)
        return queryset
