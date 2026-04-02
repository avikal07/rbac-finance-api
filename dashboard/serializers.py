from __future__ import annotations

from rest_framework import serializers


class SummarySerializer(serializers.Serializer):
    total_income = serializers.FloatField()
    total_expense = serializers.FloatField()
    net_balance = serializers.FloatField()


class CategoryTotalsQuerySerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=[("income", "income"), ("expense", "expense")], required=False)
