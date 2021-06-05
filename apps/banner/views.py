from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView

from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import utils


class HomeView(TemplateView):
    template_name = "banner/index.html"


class CampaignDetail(APIView):
    @method_decorator(cache_page(60*60*24*14))
    def get(self, request, *args, **kwargs):
        campaign = get_object_or_404(models.Campaign, pk=kwargs['pk'])
        quarter = utils.get_current_quarter()
        quarter = 1
        client_ip = request.META['REMOTE_ADDR']

        # we could also exclude more banners
        # (e.g. per day, but we'll just exclude the last one seen)
        last_banner_seen = models.BannerSeen.objects.filter(address=client_ip) \
            .order_by('-id') \
            .first()

        if not last_banner_seen:
            last_banner_seen = []
        else:
            last_banner_seen = [last_banner_seen.banner_id]

        # count banners with revenue
        num_banners = len(models.Click.objects.get_unique_banners_with_revenue(campaign, quarter, last_banner_seen))

        if num_banners >= 10:
            scenario = settings.SCENARIOS['1']
            banner_ids = utils.qs_to_list(models.Click.objects.get_top10_unique_banners_with_revenue_totals(
                campaign, quarter, last_banner_seen
            ))
        elif num_banners in range(5, 10):
            scenario = settings.SCENARIOS['2']
            banner_ids = utils.qs_to_list(models.Click.objects.get_x_unique_banners_with_revenue_totals(
                campaign, quarter, last_banner_seen, num_banners
            ))
        elif num_banners in range(1, 5):
            scenario = settings.SCENARIOS['3']
            banner_ids = utils.qs_to_list(models.Click.objects.get_x_unique_banners_with_revenue_totals(
                campaign, quarter, last_banner_seen, num_banners
            ))

            # if <5, complement with top clicks
            if num_banners < 5:
                extra_banner_ids = models.Banner.objects.get_banner_ids_by_click_count(banner_ids)[:(5-num_banners)]
                banner_ids += utils.qs_to_list(extra_banner_ids)
        else:
            scenario = settings.SCENARIOS['4']

            # check if we have enough banner with clicks
            banner_ids = utils.qs_to_list(models.Banner.objects.get_banner_ids_by_click_count(last_banner_seen))
            len_banner_ids = len(banner_ids)

            if len_banner_ids >= 5:
                banner_ids = banner_ids[:5]
            elif 5 > len_banner_ids > 0:
                num_random = 5 - len_banner_ids
                qs = models.Banner.objects.get_random_banner_ids(num_random, last_banner_seen)
                random_banners = utils.qs_to_list(qs)
                banner_ids += random_banners
            else:
                qs = models.Banner.objects.get_random_banner_ids(5, last_banner_seen)
                banner_ids = utils.qs_to_list(qs)

        for banner_id in banner_ids:
            models.BannerSeen.objects.create(
                banner_id=banner_id,
                address=client_ip
            )

        return Response({
            'banners': utils.randomize_list(banner_ids),
            'scenario': scenario,
            'num_banners': num_banners
        })
