from django.urls import path

from .views import EradListView

app_name = "erad"
urlpatterns = [
    path("", EradListView.as_view(), name="list"),
    # path("scraping", erad_scraping, name="scraping"),
    # path("export_csv", export_csv, name="export_csv"),
]
