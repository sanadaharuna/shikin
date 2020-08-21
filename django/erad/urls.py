from django.urls import path

from erad import views

app_name = "erad"
urlpatterns = [
    path("list", views.EradListView.as_view(), name="list"),
]
