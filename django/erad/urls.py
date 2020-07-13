from django.urls import path

from erad import views

app_name = "erad"
urlpatterns = [
    path("list", views.ItemListView.as_view(), name="list"),
    path("suppl_list", views.SupplListView.as_view(), name="suppl_list"),
    path("create", views.SupplCreateView.as_view(), name="create"),
    path("<int:pk>/update", views.SupplUpdateView.as_view(), name="update"),
    path("<int:pk>/delete", views.SupplDeleteView.as_view(), name="delete"),
]
