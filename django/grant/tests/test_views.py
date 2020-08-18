from django.test import TestCase
from django.urls import resolve
from grant.views import (
    GrantListView,
    GrantCreateView,
    GrantUpdateView,
    GrantDeleteView,
    GrantExportView,
)


class GrantUrlResolveTest(TestCase):
    def test_url_resolves_to_grant_list_view(self):
        view = resolve("/grant/list")
        self.assertEqual(view.func.view_class, GrantListView)

    def test_url_resolves_to_grant_create_view(self):
        view = resolve("/grant/create")
        self.assertEqual(view.func.view_class, GrantCreateView)

    def test_url_resolves_to_grant_update_view(self):
        view = resolve("/grant/1/update")
        self.assertEqual(view.func.view_class, GrantUpdateView)

    def test_url_resolves_to_grant_delete_view(self):
        view = resolve("/grant/1/delete")
        self.assertEqual(view.func.view_class, GrantDeleteView)

    def test_url_resolves_to_grant_export_view(self):
        view = resolve("/grant/export")
        self.assertEqual(view.func.view_class, GrantExportView)
