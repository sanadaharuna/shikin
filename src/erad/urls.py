from django.urls import path

from .views import EradListView

from .views import EradListView, erad_scraping


app_name = "erad"
urlpatterns = [
    path("list", EradListView.as_view(), name="list"),
    path("scraping", erad_scraping, name="scraping"),
]
