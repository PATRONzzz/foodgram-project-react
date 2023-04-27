from app.models import (
    Favorite,
    Ingredient,
    Recipe,
    Recipe_ingredient,
    ShopCard,
    Subscribe,
    Tag,
)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import BaseUserManager
from users.models import CustomUser

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, username, password, fitst_name, last_name):
#         if not email:
#             raise ValueError("Users must have an email address")

#         user = self.model(
#             email=self.normalize_email(email),
#             date_of_birth=date_of_birth,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(
#         self,
#         email,
#         username,
#         password,
#         fitst_name,
#         last_name,
#     ):
#         """
#         Creates and saves a superuser with the given email, date of
#         birth and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#             date_of_birth=date_of_birth,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


class UsersModelAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "email",
                ),
            },
        ),
    )
    list_display = ("username", "pk", "first_name", "last_name", "email")
    list_filter = ("email", "username")
    search_fields = ("email", "username")
    empty_value_display = "-пусто-"


admin.site.register(CustomUser, UsersModelAdmin)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(Recipe)
admin.site.register(Recipe_ingredient)
admin.site.register(Subscribe)
admin.site.register(ShopCard)
