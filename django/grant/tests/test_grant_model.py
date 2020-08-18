from django.test import TestCase
from grant.models import Grant
from grant.tests.factories import GrantFactory


class GrantModelTests(TestCase):
    def test_is_empty(self):
        item_list = Grant.objects.all()
        self.assertEqual(item_list.count(), 0)

    def test_is_not_empty(self):
        GrantFactory.create()
        item_list = Grant.objects.all()
        self.assertEqual(item_list.count(), 1)
