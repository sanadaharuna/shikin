from django.urls import path

from .views import EradListView, erad_scraping, export_csv

app_name = "erad"
urlpatterns = [
    path("list", EradListView.as_view(), name="list"),
    path("scraping", erad_scraping, name="scraping"),
    path("export_csv", export_csv, name="export_csv"),
]
