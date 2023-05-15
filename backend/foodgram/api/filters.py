from django_filters import rest_framework as filters
from app.models import Tag, Recipe

# class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug", to_field_name="slug", queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(method="is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(method="is_shopping_cart")

    class Meta:
        model = Recipe
        fields = (
            "tags",
            "author",
        )

`
#     def is_in_shopping_cart_filter(self, queryset, name, value):
#         user = self.request.user
#         if value and user.is_authenticated:
#             return queryset.filter(shopping_recipe__user=user)
#         return queryset

#     def is_favorited(self, queryset, name, value):
#         user = self.request.user
#         if value and user.is_authenticated:
#             return queryset.filter(favorite_recipe__user=user)
`#         return queryset
