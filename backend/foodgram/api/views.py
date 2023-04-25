from api.pagination import UserPagination
from api.serializers import UserSerializer
from app.models import Favorite, Ingredient, Recipe_ingredient, Subscribe, Tag
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from users.models import CustomUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination


class RecipeViewSet(viewsets.ModelViewSet):
    pass


class TagViewSet(viewsets.ModelViewSet):
    pass
