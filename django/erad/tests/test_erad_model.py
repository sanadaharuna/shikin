from django.test import TestCase
from erad.models import Erad, Suppl
from erad.tests.factories import NayoseFactory, ShokuinFactory


class NayoseModelTests(TestCase):
    def test_no_item(self):
        item_list = Nayose.objects.all()
        self.assertEqual(0, item_list.count())

    def test_1_item(self):
        NayoseFactory.create()
        item_list = Nayose.objects.all()
        self.assertEqual(1, item_list.count())

    # def test_age(self):
    #     today = date(2020, 5, 4)


class ShokuinModelTests(TestCase):
    def test_no_item(self):
        item_list = Shokuin.objects.all()
        self.assertEqual(0, item_list.count())

    def test_1_item(self):
        ShokuinFactory.create()
        item_list = Shokuin.objects.all()
        self.assertEqual(1, item_list.count())
