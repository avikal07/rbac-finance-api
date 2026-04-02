from __future__ import annotations

from dataclasses import dataclass

from django.db import transaction
from rest_framework.authtoken.models import Token

from users.models import User


@dataclass(frozen=True)
class AuthTokens:
    token: str


@transaction.atomic
def issue_token_for_user(*, user: User) -> AuthTokens:
    token, _ = Token.objects.get_or_create(user=user)
    return AuthTokens(token=token.key)

