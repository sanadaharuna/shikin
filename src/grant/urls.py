from django.urls import path

from .views import GrantListView

app_name = "grant"
urlpatterns = [path("list", GrantListView.as_view(), name="list")]
