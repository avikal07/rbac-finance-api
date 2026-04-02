from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from django.db.models import Count, DecimalField, QuerySet, Sum, Value
from django.db.models.functions import Coalesce, TruncMonth

from records.models import Record, RecordType
from users.models import User


def _base_qs(*, user: User) -> QuerySet[Record]:
    qs = Record.objects.alive()
    if user.role != "admin":
        qs = qs.filter(created_by=user)
    return qs


def total_income(*, user: User) -> float:
    value = (
        _base_qs(user=user)
        .filter(type=RecordType.INCOME)
        .aggregate(total=Coalesce(Sum("amount"), Value(0), output_field=DecimalField(max_digits=12, decimal_places=2)))
        .get("total")
    )
    return float(value)


def total_expense(*, user: User) -> float:
    value = (
        _base_qs(user=user)
        .filter(type=RecordType.EXPENSE)
        .aggregate(total=Coalesce(Sum("amount"), Value(0), output_field=DecimalField(max_digits=12, decimal_places=2)))
        .get("total")
    )
    return float(value)


def net_balance(*, user: User) -> float:
    return total_income(user=user) - total_expense(user=user)


def category_totals(*, user: User, record_type: str | None = None):
    qs = _base_qs(user=user)
    if record_type:
        qs = qs.filter(type=record_type)
    return list(
        qs.values("category")
        .annotate(
            total=Coalesce(Sum("amount"), Value(0), output_field=DecimalField(max_digits=12, decimal_places=2)),
            count=Count("id"),
        )
        .order_by("-total", "category")
    )


def recent_transactions(*, user: User, limit: int = 10):
    qs = _base_qs(user=user).select_related("created_by").order_by("-date", "-created_at")[:limit]
    return qs


def monthly_trends(*, user: User, months: int = 12):
    qs = _base_qs(user=user)
    # Return last N months that have data; keep simple and DB-driven.
    data = (
        qs.annotate(month=TruncMonth("date"))
        .values("month", "type")
        .annotate(total=Coalesce(Sum("amount"), Value(0), output_field=DecimalField(max_digits=12, decimal_places=2)))
        .order_by("month")
    )
    return list(data)

