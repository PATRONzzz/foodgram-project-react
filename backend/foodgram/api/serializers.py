import base64
from ast import Import
from dataclasses import field

from api.pagination import UserPagination
from app.models import CustomUser, Tag
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
        fields = ("email", "id", "username", "first_name", "last_name")


class TagSerializer(serializers.ModelSerializer):
    """[GET] Список тегов"""

    class Meta:
        model = Tag
        fields = "__all__"
