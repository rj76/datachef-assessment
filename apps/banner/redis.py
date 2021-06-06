import logging
import redis3

from django.conf import settings
from django.db.models import Count
from . import utils, models

redis = redis3.Redis(host='localhost', port=6379, db=0)
logger = logging.getLogger('apps.banner')


def store_last_banners_for_ip(banner_ids, ip):
    key = '%s-%s' % (settings.REDIS_PREFIX_LAST_BANNER_FOR_IP, ip)
    redis.delete(key)
    store_list(key, banner_ids)


def get_last_banners_for_ip(ip):
    key = '%s-%s' % (settings.REDIS_PREFIX_LAST_BANNER_FOR_IP, ip)
    return get_list(key)


def get_random_banner_ids(count, exclude_banner_ids):
    key = '%s' % settings.REDIS_PREFIX_RANDOM_BANNERS
    banner_ids = get_list(key)
    banner_ids = utils.randomize_list(banner_ids)
    return [id for id in banner_ids if id not in exclude_banner_ids][:count]


def get_banner_ids_by_click_count(exclude_banner_ids):
    key = '%s' % settings.REDIS_PREFIX_TOP10_BY_CLICKS
    banner_ids = get_list(key)
    return [id for id in banner_ids if id not in exclude_banner_ids]


def get_unique_banners_with_revenue(campaign, quarter, exclude_banner_ids):
    key = '%s-%s-%s' % (settings.REDIS_PREFIX_UNIQUE_WITH_REVENUE, campaign.pk, quarter)
    banner_ids = get_list(key)
    return [id for id in banner_ids if id not in exclude_banner_ids]


def get_topX_unique_banners_with_revenue_totals(x, campaign, quarter, banners_seen):
    key = '%s-%s-%s' % (settings.REDIS_PREFIX_TOP10_BY_REVENUE, campaign.pk, quarter)
    result = get_list(key)
    result = [id for id in result if id not in banners_seen][:x]

    return result


def fill_redis():
    redis.flushdb()
    for quarter in range(1, 5):
        # unique with revenue
        for campaign in models.Campaign.objects.all():
            banner_ids_qs = models.Click.objects \
                .filter(campaign=campaign, quarter=quarter, conversions__revenue__gt=0) \
                .values('banner_id') \
                .distinct()

            key = '%s-%s-%s' % (settings.REDIS_PREFIX_UNIQUE_WITH_REVENUE, campaign.pk, quarter)
            banner_ids = [b['banner_id'] for b in banner_ids_qs]
            logger.info('unique with revenue: storing %d banners for key: %s' % (len(banner_ids), key))
            store_list(key, banner_ids)

            # top 10 by revenue
            banner_ids_qs = models.Click.objects.filter(banner_id__in=banner_ids) \
                .values('banner_id') \
                .distinct() \
                .order_by('-conversion_revenue_sum') \
                .values('banner_id').distinct()[:1000]

            key = '%s-%s-%s' % (settings.REDIS_PREFIX_TOP10_BY_REVENUE, campaign.pk, quarter)
            top10_banner_ids = [b['banner_id'] for b in banner_ids_qs]
            logger.info('top 10 by revenue: storing %d banners for key: %s' % (len(top10_banner_ids), key))
            store_list(key, top10_banner_ids)

    # random
    random_qs = models.Banner.objects.all() \
        .order_by('?') \
        .values('banner_id')[:10]

    key = '%s' % settings.REDIS_PREFIX_RANDOM_BANNERS
    random_banner_ids = [b['banner_id'] for b in random_qs]
    logger.info('random: storing %d banners for key: %s' % (len(random_banner_ids), key))
    store_list(key, random_banner_ids)

    # top 10 clicks
    top10_by_clicks_qs = models.Banner.objects.all() \
        .annotate(count=Count('clicks')) \
        .filter(count__gt=0) \
        .order_by('-count') \
        .values('banner_id') \
        .distinct()[:10]

    key = '%s' % settings.REDIS_PREFIX_TOP10_BY_CLICKS
    top10_by_clicks_banner_ids = [b['banner_id'] for b in top10_by_clicks_qs]
    logger.info('top 10 clicks: storing %d banners for key: %s' % (len(top10_by_clicks_banner_ids), key))
    store_list(key, top10_by_clicks_banner_ids)


def store_list(key, _list):
    if not _list:
        return

    redis.lpush(key, *_list)


def get_list(key):
    result = redis.lrange(key, 0, -1)
    if not result:
        return []

    return [v.decode('utf-8') for v in result]
