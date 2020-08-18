import factory
import factory.django
import factory.fuzzy

from grant.models import Grant


class GrantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Grant

    accepted_at = factory.Faker("date")
    zaidanmei = factory.Faker("company")
    koubomei = factory.Faker("company")
    url = factory.Faker("url")
    torimatome = factory.fuzzy.FuzzyChoice(
        Grant.ARRANGE, getter=lambda c: c[0])
    bikou = factory.Faker("lorem")
