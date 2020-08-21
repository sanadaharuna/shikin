from django.test import TestCase
from erad.models import Erad
from erad.tests.factories import EradFactory


class EradModelTests(TestCase):
    def test_is_empty(self):
        item_list = Erad.objects.all()
        self.assertEqual(item_list.count(), 0)

    def test_is_not_empty(self):
        EradFactory.create()
        item_list = Erad.objects.all()
        self.assertEqual(item_list.count(), 1)
