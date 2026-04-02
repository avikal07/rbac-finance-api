from __future__ import annotations

from django.urls import path

from dashboard.views import (
    DashboardCategoryTotalsView,
    DashboardMonthlyTrendsView,
    DashboardRecentTransactionsView,
    DashboardSummaryView,
)

# urlpatterns = [
#     path("dashboard/summary/", DashboardSummaryView.as_view(), name="dashboard-summary"),
#     path("dashboard/category-totals/", DashboardCategoryTotalsView.as_view(), name="dashboard-category-totals"),
#     path("dashboard/recent-transactions/", DashboardRecentTransactionsView.as_view(), name="dashboard-recent-transactions"),
#     path("dashboard/monthly-trends/", DashboardMonthlyTrendsView.as_view(), name="dashboard-monthly-trends"),
# ]

urlpatterns = [
    path("summary/", DashboardSummaryView.as_view(), name="dashboard-summary"),
    path("category-totals/", DashboardCategoryTotalsView.as_view(), name="dashboard-category-totals"),
    path("recent-transactions/", DashboardRecentTransactionsView.as_view(), name="dashboard-recent-transactions"),
    path("monthly-trends/", DashboardMonthlyTrendsView.as_view(), name="dashboard-monthly-trends"),
]