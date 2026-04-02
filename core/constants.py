from __future__ import annotations


class Roles:
    VIEWER = "viewer"
    ANALYST = "analyst"
    ADMIN = "admin"

    CHOICES = (
        (VIEWER, "Viewer"),
        (ANALYST, "Analyst"),
        (ADMIN, "Admin"),
    )

