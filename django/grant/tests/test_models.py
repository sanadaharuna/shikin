from django.test import TestCase
from grant.models import Grant


class GrantModelTests(TestCase):
    def test_is_empty(self):
        saved_grants = Grant.objects.all()
        self.assertEqual(saved_grants.count(), 0)
