from __future__ import annotations

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class RecordType(models.TextChoices):
    INCOME = "income", "Income"
    EXPENSE = "expense", "Expense"


class RecordQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(is_deleted=False)


class Record(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    type = models.CharField(max_length=10, choices=RecordType.choices)
    category = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="records")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    objects = RecordQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=["type", "date"]),
            models.Index(fields=["category"]),
            models.Index(fields=["created_by", "date"]),
        ]
        ordering = ["-date", "-created_at"]

    def soft_delete(self):
        self.is_deleted = True
        self.save(update_fields=["is_deleted", "updated_at"])
