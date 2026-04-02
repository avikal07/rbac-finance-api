from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from django.db.models import QuerySet

from records.models import Record, RecordType
from users.models import User


@dataclass(frozen=True)
class RecordFilters:
    type: str | None = None
    category: str | None = None
    date_from: date | None = None
    date_to: date | None = None


def list_records(*, requesting_user: User, filters: RecordFilters) -> QuerySet[Record]:
    qs = Record.objects.alive().select_related("created_by")

    # Access rules: viewers/analysts/admins can read records, but should only see all records
    # if they are admin; otherwise, scope to their own.
    if requesting_user.role != "admin":
        qs = qs.filter(created_by=requesting_user)

    if filters.type:
        qs = qs.filter(type=filters.type)
    if filters.category:
        qs = qs.filter(category__iexact=filters.category.strip())
    if filters.date_from:
        qs = qs.filter(date__gte=filters.date_from)
    if filters.date_to:
        qs = qs.filter(date__lte=filters.date_to)

    return qs


def create_record(*, requesting_user: User, payload: dict) -> Record:
    return Record.objects.create(created_by=requesting_user, **payload)


def update_record(*, record: Record, payload: dict) -> Record:
    for field, value in payload.items():
        setattr(record, field, value)
    record.save()
    return record


def delete_record(*, record: Record) -> None:
    record.soft_delete()


def parse_record_filters(*, query_params) -> RecordFilters:
    """
    Keep query parsing centralized so views stay thin.
    """
    record_type = query_params.get("type") or None
    if record_type and record_type not in {RecordType.INCOME, RecordType.EXPENSE}:
        record_type = None

    category = query_params.get("category") or None
    date_from = query_params.get("date_from") or None
    date_to = query_params.get("date_to") or None

    def parse_date(value: str | None) -> date | None:
        if not value:
            return None
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None

    return RecordFilters(
        type=record_type,
        category=category,
        date_from=parse_date(date_from),
        date_to=parse_date(date_to),
    )

