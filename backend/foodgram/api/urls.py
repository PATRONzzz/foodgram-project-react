from api.views import UserViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    # path(r"auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),
]
