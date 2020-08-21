from django.test import TestCase
from django.urls import resolve
from erad.views import EradListView


class EradUrlResolveTest(TestCase):
    def test_url_resolves_to_erad_list_view(self):
        view = resolve("/erad/list")
        self.assertEqual(view.func.view_class, EradListView)
