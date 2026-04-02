from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import LoginView, MeView, UserAdminViewSet

router = DefaultRouter()
router.register(r"admin/users", UserAdminViewSet, basename="admin-users")

# urlpatterns = [
#     path("auth/login/", LoginView.as_view(), name="login"),
#     path("auth/me/", MeView.as_view(), name="me"),
#     path("", include(router.urls)),
# ]

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("me/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
]