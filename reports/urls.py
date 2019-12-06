from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:report_id>", views.report, name="report"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("dashboard_report/<int:dashboard_report_id>", views.dashboard_report, name="dashboard_report"),
    path("reports", views.reports, name="reports"),
]