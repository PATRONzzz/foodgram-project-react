from app.models import (Favorite, Ingredient, Recipe, Recipe_ingredient,
                        ShopCart, Subscribe, Tag)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser


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
admin.site.register(ShopCart)
