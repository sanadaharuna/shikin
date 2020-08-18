from django.test import TestCase
from django.urls import resolve
from erad.views import (
    ItemListView,
    SupplListView,
    SupplCreateView,
    SupplUpdateView,
    SupplDeleteView,
)


class EradUrlResolveTest(TestCase):
    def test_url_resolves_to_item_list_view(self):
        view = resolve("/erad/list")
        self.assertEqual(view.func.view_class, ItemListView)

    def test_url_resolves_to_suppl_list_view(self):
        view = resolve("/erad/suppl_list")
        self.assertEqual(view.func.view_class, SupplListView)

    def test_url_resolves_to_suppl_create_view(self):
        view = resolve("/erad/create")
        self.assertEqual(view.func.view_class, SupplCreateView)

    def test_url_resolves_to_suppl_update_view(self):
        view = resolve("/erad/1/update")
        self.assertEqual(view.func.view_class, SupplUpdateView)

    def test_url_resolves_to_suppl_delete_view(self):
        view = resolve("/erad/1/delete")
        self.assertEqual(view.func.view_class, SupplDeleteView)
