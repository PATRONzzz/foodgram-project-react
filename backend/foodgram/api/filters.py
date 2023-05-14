from django_filters import rest_framework as filters
from reviews.models import Title

# class FilterForTitle(filters.FilterSet):
#     name = filters.CharFilter(field_name='name',
#                               lookup_expr='contains')
#     category = filters.CharFilter(field_name='category__slug',
#                                   lookup_expr='exact')
#     genre = filters.CharFilter(field_name='genre__slug',
#                                lookup_expr='exact')

#     class Meta:
#         model = Title
#         fields = ('name', 'category', 'genre', 'year',)


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)


#  queryset = self.queryset

#         tags: list = self.request.query_params.getlist(UrlQueries.TAGS.value)
#         if tags:
#             queryset = queryset.filter(
#                 tags__slug__in=tags).distinct()

#         author: str = self.request.query_params.get(UrlQueries.AUTHOR.value)
#         if author:
#             queryset = queryset.filter(author=author)

#         if self.request.user.is_anonymous:
#             return queryset

#         is_in_cart: str = self.request.query_params.get(UrlQueries.SHOP_CART)
#         if is_in_cart in Tuples.SYMBOL_TRUE_SEARCH.value:
#             queryset = queryset.filter(in_carts__user=self.request.user)
#         elif is_in_cart in Tuples.SYMBOL_FALSE_SEARCH.value:
#             queryset = queryset.exclude(in_carts__user=self.request.user)

#         is_favorite: str = self.request.query_params.get(UrlQueries.FAVORITE)
#         if is_favorite in Tuples.SYMBOL_TRUE_SEARCH.value:
#             queryset = queryset.filter(in_favorites__user=self.request.user)
#         if is_favorite in Tuples.SYMBOL_FALSE_SEARCH.value:
#             queryset = queryset.exclude(in_favorites__user=self.request.user)

#         return


class AccountTFilter(filters.FilterSet):
    # could alternatively use IsoDateTimeFilter instead of assuming local time.
    created_date = filters.DateTimeFilter(
        name="created_date_t", method="filter_timestamp"
    )

    class Meta:
        model = models.AccountT
        # 'filterset_fields' simply proxies the 'Meta.fields' option
        # Also, it isn't necessary to include declared fields here
        fields = ["othermodelfield"]

    def filter_timestamp(self, queryset, name, value):
        # transform datetime into timestamp
        value = ...

        return queryset.filter(**{name: value})


# class RecipeFilter(FilterSet):
#     tags = filters.ModelMultipleChoiceFilter(
#         field_name="tags__slug", to_field_name="slug", queryset=Tag.objects.all()
#     )
#     is_favorited = filters.BooleanFilter(method="is_favorited_filter")
#     is_in_shopping_cart = filters.BooleanFilter(method="is_in_shopping_cart_filter")

#     class Meta:
#         model = Recipe
#         fields = (
#             "tags",
#             "author",
#         )

#     def is_favorited_filter(self, queryset, name, value):
#         user = self.request.user
#         if value and user.is_authenticated:
#             return queryset.filter(favorite_recipe__user=user)
#         return queryset

#     def is_in_shopping_cart_filter(self, queryset, name, value):
#         user = self.request.user
#         if value and user.is_authenticated:
#             return queryset.filter(shopping_recipe__user=user)
#         return queryset
