from api.views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("tags", TagViewSet)
router.register("recipes", RecipeViewSet)
router.register("ingridients", IngredientViewSet)


urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),
]
