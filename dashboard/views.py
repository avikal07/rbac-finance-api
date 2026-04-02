from __future__ import annotations

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import ROLE_POLICY_DASHBOARD, RolePermission
from dashboard.serializers import CategoryTotalsQuerySerializer, SummarySerializer
from dashboard.services import (
    category_totals,
    monthly_trends,
    net_balance,
    recent_transactions,
    total_expense,
    total_income,
)
from records.serializers import RecordSerializer


class DashboardSummaryView(APIView):
    permission_classes = [RolePermission]
    role_policy = ROLE_POLICY_DASHBOARD

    def get(self, request):
        data = {
            "total_income": total_income(user=request.user),
            "total_expense": total_expense(user=request.user),
            "net_balance": net_balance(user=request.user),
        }
        serializer = SummarySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class DashboardCategoryTotalsView(APIView):
    permission_classes = [RolePermission]
    role_policy = ROLE_POLICY_DASHBOARD

    def get(self, request):
        qs = CategoryTotalsQuerySerializer(data=request.query_params)
        qs.is_valid(raise_exception=True)
        record_type = qs.validated_data.get("type")
        return Response({"results": category_totals(user=request.user, record_type=record_type)})


class DashboardRecentTransactionsView(APIView):
    permission_classes = [RolePermission]
    role_policy = ROLE_POLICY_DASHBOARD

    def get(self, request):
        limit_raw = request.query_params.get("limit", "10")
        try:
            limit = max(1, min(int(limit_raw), 100))
        except ValueError:
            limit = 10
        qs = recent_transactions(user=request.user, limit=limit)
        return Response({"results": RecordSerializer(qs, many=True).data})


class DashboardMonthlyTrendsView(APIView):
    permission_classes = [RolePermission]
    role_policy = ROLE_POLICY_DASHBOARD

    def get(self, request):
        return Response({"results": monthly_trends(user=request.user)})
