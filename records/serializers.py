from __future__ import annotations

from rest_framework import serializers

from records.models import Record, RecordType


class RecordSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Record
        fields = (
            "id",
            "amount",
            "type",
            "category",
            "date",
            "description",
            "created_by",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_by", "created_at", "updated_at")

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value

    def validate_type(self, value: str) -> str:
        valid = {RecordType.INCOME, RecordType.EXPENSE}
        if value not in valid:
            raise serializers.ValidationError("Type must be 'income' or 'expense'.")
        return value

    def validate_category(self, value: str) -> str:
        value = (value or "").strip()
        if not value:
            raise serializers.ValidationError("Category is required.")
        return value

