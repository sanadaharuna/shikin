from django.urls import path

from .views import GrantListView, export_csv

app_name = "grant"
urlpatterns = [
    path("list", GrantListView.as_view(), name="list"),
    path("export_csv", export_csv, name="export_csv"),
]
