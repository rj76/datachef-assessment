import pytest
import random

from django.conf import settings
from django.urls import reverse

from rest_framework import status

from . import factories
from apps.banner import models, utils


@pytest.mark.django_db
class TestApi:
    def test_top10(self, client):
        # more than 10 banners with revenue, should return top 10 banners
        num_banners = random.randrange(10, 20, 1)
        campaign = factories.CampaignFactory()
        banners = [factories.BannerFactory(banner_id=i) for i in range(1, 101)]
        # create database entries
        self.create_data_with_revenue(campaign, num_banners, banners)

        response = client.get(reverse('campaign', kwargs={'pk': campaign.campaign_id}))
        assert response.status_code == status.HTTP_200_OK

        assert response.data['scenario'] == settings.SCENARIOS['1']
        assert len(response.data['banners']) == 10

    def test_range_5_10(self, client):
        # x between 5 and 10 banners with revenue, should return top x banners
        num_banners = random.randrange(5, 10, 1)
        campaign = factories.CampaignFactory()
        banners = [factories.BannerFactory(banner_id=i) for i in range(1, 11)]

        # create database entries
        self.create_data_with_revenue(campaign, num_banners, banners)

        response = client.get(reverse('campaign', kwargs={'pk': campaign.campaign_id}))
        assert response.status_code == status.HTTP_200_OK

        assert response.data['scenario'] == settings.SCENARIOS['2']
        assert len(response.data['banners']) == num_banners

    def test_range_1_5(self, client):
        # x between 1 and 5 banners with revenue, should return top x banners
        num_banners = random.randrange(1, 5, 1)
        campaign = factories.CampaignFactory()
        banners = [factories.BannerFactory(banner_id=i) for i in range(1, 11)]

        # create database entries
        self.create_data_with_revenue(campaign, num_banners, banners)

        if num_banners < 5:
            # add clicks
            clicks_needed = 5 - num_banners
            exclude_banner_ids = models.Click.objects.get_unique_banners_with_revenue(campaign, 1, [])
            extra_banner_ids = utils.qs_to_list(models.Banner.objects.get_banner_ids_by_click_count(exclude_banner_ids))

            # create extra clicks?
            if len(extra_banner_ids) < clicks_needed:
                max_id = num_banners + 10

                for i in range(0, clicks_needed+5):
                    banner = [banner for banner in banners if banner.banner_id not in extra_banner_ids][0]
                    extra_banner_ids.append(banner.banner_id)

                    factories.ClickFactory(
                        click_id=max_id+1,
                        banner=banner,
                        campaign=campaign,
                    )

                    max_id += 1

        response = client.get(reverse('campaign', kwargs={'pk': campaign.campaign_id}))
        assert response.status_code == status.HTTP_200_OK

        assert response.data['scenario'] == settings.SCENARIOS['3']
        assert len(response.data['banners']) == 5

    def test_no_banners_with_revenue_with_enough_clicks(self, client):
        # Show the top5 banners based on clicks.
        # If the amount of banners with clicks are less than 5 within that campaign,
        # then you should add random banners to make up a collection of 5 unique banners.
        campaign = factories.CampaignFactory()
        banners = [factories.BannerFactory(banner_id=i) for i in range(1, 11)]

        i = count = 0
        while count <= 4:
            banner = banners[random.randrange(0, len(banners), 1)]

            factories.ClickFactory(
                click_id=i+1,
                banner=banner,
                campaign=campaign,
            )

            count = len(models.Banner.objects.get_banner_ids_by_click_count([]))
            i += 1

        response = client.get(reverse('campaign', kwargs={'pk': campaign.campaign_id}))
        assert response.status_code == status.HTTP_200_OK

        assert response.data['scenario'] == settings.SCENARIOS['4']
        assert len(response.data['banners']) == 5

    def test_no_banners_with_revenue_not_enough_clicks(self, client):
        # Show the top5 banners based on clicks.
        # If the amount of banners with clicks are less than 5 within that campaign,
        # then you should add random banners to make up a collection of 5 unique banners.
        campaign = factories.CampaignFactory()
        banners = [factories.BannerFactory(banner_id=i) for i in range(1, 11)]

        i = count = 0
        while count <= 2:
            banner = banners[random.randrange(0, len(banners), 1)]

            factories.ClickFactory(
                click_id=i+1,
                banner=banner,
                campaign=campaign,
            )

            count = len(models.Banner.objects.get_banner_ids_by_click_count([]))
            i += 1

        response = client.get(reverse('campaign', kwargs={'pk': campaign.campaign_id}))
        assert response.status_code == status.HTTP_200_OK

        assert response.data['scenario'] == settings.SCENARIOS['4']
        assert len(response.data['banners']) == 5

    def test_no_banners_with_revenue_no_clicks(self, client):
        # Show the top5 banners based on clicks.
        # If the amount of banners with clicks are less than 5 within that campaign,
        # then you should add random banners to make up a collection of 5 unique banners.
        campaign = factories.CampaignFactory()
        [factories.BannerFactory(banner_id=i) for i in range(1, 11)]

        response = client.get(reverse('campaign', kwargs={'pk': campaign.campaign_id}))
        assert response.status_code == status.HTTP_200_OK

        assert response.data['scenario'] == settings.SCENARIOS['4']
        assert len(response.data['banners']) == 5

    def create_data_with_revenue(self, campaign, num_banners, banners):
        i = count = 0
        while count < num_banners:
            banner = banners[int(random.randrange(0, len(banners)))]
            click = factories.ClickFactory(
                click_id=i+3,
                banner=banner,
                campaign=campaign,
            )

            factories.ConversionFactory(
                conversion_id=i+2,
                click=click,
                revenue=1
            )

            count = len(models.Click.objects.get_unique_banners_with_revenue(campaign, 1, []))
            i += 1
