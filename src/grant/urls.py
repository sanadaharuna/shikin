from django.urls import path

from grant.views import GrantExportView, GrantListView

app_name = "grant"
urlpatterns = [
    path("", GrantListView.as_view(), name="list"),
    # path("export_csv", export_csv, name="export_csv"),
    path("export", GrantExportView.as_view(), name="export"),
]
