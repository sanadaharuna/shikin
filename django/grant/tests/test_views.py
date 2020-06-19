from django.test import TestCase
from django.urls import resolve, reverse
from grant.views import GrantListView


class UrlTest(TestCase):
    def test_grant_list_view_status_code(self):
        url = reverse("grant:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_grant_list_url_resolves_to_list_view(self):
        view = resolve("grant/")
        self.assertEqual(view.func, GrantListView)
