from __future__ import annotations

from dataclasses import dataclass

from rest_framework.permissions import BasePermission, SAFE_METHODS

from core.constants import Roles


@dataclass(frozen=True)
class RolePolicy:
    read_roles: frozenset[str]
    write_roles: frozenset[str]

    @classmethod
    def read_only(cls, *, allowed_roles: set[str] | frozenset[str]) -> "RolePolicy":
        roles = frozenset(allowed_roles)
        return cls(read_roles=roles, write_roles=frozenset())

    @classmethod
    def crud(cls, *, read_roles: set[str] | frozenset[str], write_roles: set[str] | frozenset[str]) -> "RolePolicy":
        return cls(read_roles=frozenset(read_roles), write_roles=frozenset(write_roles))


class RolePermission(BasePermission):
    """
    Reusable role-based permission.

    Views must define:
      - role_policy: RolePolicy

    Enforcement:
      - SAFE_METHODS -> role_policy.read_roles
      - non-safe -> role_policy.write_roles
    """

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False

        policy: RolePolicy | None = getattr(view, "role_policy", None)
        if policy is None:
            return False

        user_role = getattr(user, "role", None)

        if user_role is None:
            return False
        if request.method in SAFE_METHODS:
            return user_role in policy.read_roles
        return user_role in policy.write_roles


ROLE_POLICY_RECORDS = RolePolicy.crud(
    read_roles={Roles.VIEWER, Roles.ANALYST, Roles.ADMIN},
    write_roles={Roles.ADMIN},
)

ROLE_POLICY_DASHBOARD = RolePolicy.read_only(
    allowed_roles={Roles.ANALYST, Roles.ADMIN},
)

ROLE_POLICY_USERS_ADMIN_ONLY = RolePolicy.crud(
    read_roles={Roles.ADMIN},
    write_roles={Roles.ADMIN},
)

