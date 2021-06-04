import factory
from factory import fuzzy

from apps.banner import models


class BannerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Banner

    banner_id = fuzzy.FuzzyInteger(1)


class CampaignFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Campaign

    campaign_id = fuzzy.FuzzyInteger(1)


class ImpressionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Impression

    quarter = fuzzy.FuzzyInteger(1, high=4)
    banner = factory.SubFactory(BannerFactory)
    campaign = factory.SubFactory(CampaignFactory)


class ClickFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Click

    click_id = fuzzy.FuzzyInteger(1)
    quarter = fuzzy.FuzzyInteger(1, high=4)
    num_impressions = fuzzy.FuzzyInteger(1)
    banner = factory.SubFactory(BannerFactory)
    campaign = factory.SubFactory(CampaignFactory)


class ConversionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Conversion

    conversion_id = fuzzy.FuzzyInteger(1)
    click = factory.SubFactory(ClickFactory)
    revenue = fuzzy.FuzzyDecimal(0, high=3)
