from __future__ import annotations

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import ROLE_POLICY_USERS_ADMIN_ONLY, RolePermission
from users.serializers import LoginSerializer, UserCreateSerializer, UserSerializer
from users.services import issue_token_for_user
from users.models import User


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = issue_token_for_user(user=user)
        return Response({"token": token.token}, status=status.HTTP_200_OK)


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserAdminViewSet(viewsets.ModelViewSet):
    """
    Admin-only user management.
    """

    queryset = User.objects.all().order_by("-date_joined")
    permission_classes = [RolePermission]
    role_policy = ROLE_POLICY_USERS_ADMIN_ONLY

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer
