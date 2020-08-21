from grant.models import Grant
from django.test import TestCase
from django.urls import resolve
from grant.views import (
    GrantListView,
    GrantCreateView,
    GrantUpdateView,
    GrantDeleteView,
    GrantExportView,
)
from django.contrib.auth import get_user_model
from datetime import date
from django.urls import reverse_lazy


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


class LoggedInTestCase(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            username="user1",
            email="user1@localhost",
            password="password"
        )
        self.client.login(username="user1", password="password")


class TestGrantCreateView(LoggedInTestCase):
    def test_create_grant_success(self):
        params = {"accepted_at": date.today(), "zaidanmei": "テスト財団", "koubomei": "テスト公募",
                  "url": "http://www.example.com", "torimatome": "1", "bikou": "備考テスト"}
        response = self.client.post(reverse_lazy("grant:create"), params)
        self.assertRedirects(response, reverse_lazy("grant:list"))
        self.assertEqual(Grant.objects.filter(zaidanmei="テスト財団").count(), 1)

    def test_create_grant_failure(self):
        response = self.client.post(reverse_lazy("grant:create"))
        self.assertFormError(response, "form", "zaidanmei", "このフィールドは必須です。")


class TestGrantUpdateView(LoggedInTestCase):
    def test_update_grant_success(self):
        grant = Grant.objects.create(accepted_at=date.today(
        ), zaidanmei="財団名変更前", koubomei="テスト公募", url="http://www.example.com", torimatome="1", bikou="備考テスト")
        params = {"accepted_at": date.today(), "zaidanmei": "財団名変更後", "koubomei": "テスト公募",
                  "url": "http://www.example.com", "torimatome": "1", "bikou": "備考テスト"}
        response = self.client.post(reverse_lazy(
            "grant:update", kwargs={"pk": grant.pk}), params)
        self.assertRedirects(response, reverse_lazy("grant:list"))
        self.assertEqual(Grant.objects.get(pk=grant.pk).zaidanmei, "財団名変更後")

    def test_update_grant_failure(self):
        response = self.client.post(reverse_lazy(
            "grant:update", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, 404)


class TestGrantDeleteView(LoggedInTestCase):
    def test_delete_grant_success(self):
        grant = Grant.objects.create(accepted_at=date.today(
        ), zaidanmei="テスト財団名", koubomei="テスト公募", url="http://www.example.com", torimatome="1", bikou="備考テスト")
        response = self.client.post(reverse_lazy(
            "grant:delete", kwargs={"pk": grant.pk}))
        self.assertRedirects(response, reverse_lazy("grant:list"))
        self.assertEqual(Grant.objects.filter(pk=grant.pk).count(), 0)

    def test_delete_grant_failure(self):
        response = self.client.post(reverse_lazy(
            "grant:delete", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, 404)
