from django.urls import path

from erad import views

app_name = "erad"
urlpatterns = [
    path("list", views.ItemListView.as_view(), name="list"),
    path("create", views.JspsCreateView.as_view(), name="create"),
    path("<int:pk>/update", views.JspsUpdateView.as_view(), name="update"),
    path("<int:pk>/delete", views.JspsDeleteView.as_view(), name="delete"),
]
