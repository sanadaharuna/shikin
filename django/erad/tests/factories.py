import factory
from factory import fuzzy
import factory.django
import factory.fuzzy
from datetime import date
from erad.models import Erad


class EradFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Erad

    erad_key = fuzzy.FuzzyText(length=7)
    erad_url = fuzzy.FuzzyText(length=100)
    url = fuzzy.FuzzyText(length=100)
    publishing_date = fuzzy.FuzzyDate(start_date=date.today())
    funding_agency = fuzzy.FuzzyText(length=20)
    call_for_applications = fuzzy.FuzzyText(length=30)
    application_unit = fuzzy.FuzzyText(length=10)
    approved_institution = fuzzy.FuzzyText(length=10)
    opening_date = fuzzy.FuzzyDate(start_date=date.today())
    closing_date = fuzzy.FuzzyDate(start_date=date.today())
