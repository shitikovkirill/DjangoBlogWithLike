from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework import routers
from apps.accounts.views import UserViewSet


router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

api_patterns = (
    [path("token/", views.obtain_auth_token), path("", include(router.urls))],
    "api",
)

urlpatterns = [path("", admin.site.urls), path("api/", include(api_patterns))]
