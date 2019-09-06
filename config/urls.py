from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from apps.accounts.views import UserViewSet
from rest_framework_jwt import views as jwtViews


router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

api_patterns = (
    [
        path("token/", jwtViews.obtain_jwt_token),
        path("token-refresh/", jwtViews.refresh_jwt_token),
        path("token-verify/", jwtViews.verify_jwt_token),
        path("", include(router.urls)),
    ],
    "api",
)

urlpatterns = [path("", admin.site.urls), path("api/", include(api_patterns))]
