from django.urls import path

from grant import views

app_name = "grant"
urlpatterns = [
    path("list", views.GrantListView.as_view(), name="list"),
    path("create", views.GrantCreateView.as_view(), name="create"),
    path("<int:pk>/update", views.GrantUpdateView.as_view(), name="update"),
    path("<int:pk>/delete", views.GrantDeleteView.as_view(), name="delete"),
    path("export", views.GrantExportView.as_view(), name="export"),
]
