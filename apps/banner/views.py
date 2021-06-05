import logging

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, utils, redis

logger = logging.getLogger('apps.banner')


class HomeView(TemplateView):
    template_name = "banner/index.html"


class CampaignDetail(APIView):
    def get(self, request, *args, **kwargs):
        campaign = get_object_or_404(models.Campaign, pk=kwargs['pk'])
        quarter = request.GET.get('quarter', utils.get_current_quarter())
        print('quarter: %s' % quarter)
        logger.info('quarter: %s' % quarter)
        client_ip = request.META['REMOTE_ADDR']

        last_banner_seen = redis.get_last_banners_for_ip(client_ip)

        # count banners with revenue
        num_banners = len(redis.get_unique_banners_with_revenue(campaign, quarter, last_banner_seen))
        print('num_banners: %d' % num_banners)
        logger.info('num_banners: %d' % num_banners)

        if num_banners >= 10:
            scenario = settings.SCENARIOS['1']
            banner_ids = utils.qs_to_list(redis.get_topX_unique_banners_with_revenue_totals(
                10, campaign, quarter, last_banner_seen
            ))

            logger.info('scenario 1: %s' % scenario)
            self.store_banners_seen(banner_ids, client_ip)
            return self.return_response(banner_ids, scenario, num_banners)

        if num_banners in range(5, 10):
            scenario = settings.SCENARIOS['2']
            banner_ids = utils.qs_to_list(redis.get_topX_unique_banners_with_revenue_totals(
                num_banners, campaign, quarter, last_banner_seen
            ))

            logger.info('scenario 2: %s' % scenario)
            self.store_banners_seen(banner_ids, client_ip)
            return self.return_response(banner_ids, scenario, num_banners)

        if num_banners in range(1, 5):
            scenario = settings.SCENARIOS['3']
            banner_ids = utils.qs_to_list(redis.get_topX_unique_banners_with_revenue_totals(
                num_banners, campaign, quarter, last_banner_seen
            ))

            logger.info('scenario 3: %s' % scenario)

            # if <5, complement with top clicks
            if num_banners < 5:
                logger.info('  not enough banners: %d (need 5)' % num_banners)
                exclude = last_banner_seen + banner_ids
                extra_banner_ids = redis.get_banner_ids_by_click_count(exclude)[:(5-num_banners)]
                banner_ids += utils.qs_to_list(extra_banner_ids)

                logger.info(' added %d extra banners from top clicks' % extra_banner_ids)


            self.store_banners_seen(banner_ids, client_ip)
            return self.return_response(banner_ids, scenario, num_banners)

        scenario = settings.SCENARIOS['4']

        # check if we have enough banner with clicks
        banner_ids = utils.qs_to_list(redis.get_banner_ids_by_click_count(last_banner_seen))
        len_banner_ids = len(banner_ids)

        logger.info('scenario 4: %s' % scenario)
        logger.info('  num_banners from top clicks: %d' % len_banner_ids)

        if len_banner_ids >= 5:
            banner_ids = banner_ids[:5]
            logger.info('  taking first 5 top clicks')
        elif 5 > len_banner_ids > 0:
            num_random = 5 - len_banner_ids
            qs = redis.get_random_banner_ids(num_random, last_banner_seen)
            random_banners = utils.qs_to_list(qs)
            banner_ids += random_banners
            logger.info('  adding %d random banners')
        else:
            qs = redis.get_random_banner_ids(5, last_banner_seen)
            banner_ids = utils.qs_to_list(qs)
            logger.info('  using 5 random banners')

        self.store_banners_seen(banner_ids, client_ip)
        return self.return_response(banner_ids, scenario, num_banners)

    def return_response(self, banner_ids, scenario, num_banners):
        return Response({
            'banners': utils.randomize_list(banner_ids),
            'scenario': scenario,
            'num_banners': num_banners
        })

    def store_banners_seen(self, banner_ids, ip):
        redis.store_last_banners_for_ip(banner_ids, ip)
