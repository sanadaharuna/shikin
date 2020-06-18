from django.urls import path

from .views import EradListView

app_name = "erad"
urlpatterns = [
    path("", EradListView.as_view(), name="list"),
]
