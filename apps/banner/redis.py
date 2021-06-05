import json
import redis3

from django.conf import settings
from django.db.models import Count
from . import utils, models


r = redis3.Redis(host='localhost', port=6379, db=0)


def store_last_banners_for_ip(banner_ids, ip):
    key = '%s-%s' % (settings.REDIS_PREFIX_LAST_BANNER_FOR_IP, ip)
    r.set(key, json.dumps(banner_ids))


def get_last_banners_for_ip(ip):
    key = '%s-%s' % (settings.REDIS_PREFIX_LAST_BANNER_FOR_IP, ip)
    banner_ids = r.get(key)
    if not banner_ids:
        return []

    return json.loads(r.get(key).decode('utf-8'))


def get_random_banner_ids(count, exclude_banner_ids):
    key = '%s' % settings.REDIS_PREFIX_RANDOM_BANNERS
    banner_ids = utils.randomize_list(json.loads(r.get(key).decode('utf-8')))
    return [id for id in banner_ids if id not in exclude_banner_ids][:count]


def get_banner_ids_by_click_count(exclude_banner_ids):
    key = '%s' % settings.REDIS_PREFIX_TOP10_BY_CLICKS
    banner_ids = json.loads(r.get(key).decode('utf-8'))
    return [id for id in banner_ids if id not in exclude_banner_ids]


def get_unique_banners_with_revenue(campaign, quarter, exclude_banner_ids):
    key = '%s-%s-%s' % (settings.REDIS_PREFIX_UNIQUE_WITH_REVENUE, campaign, quarter)
    redis_value = r.get(key)
    if not redis_value:
        return []

    banner_ids = json.loads(redis_value.decode('utf-8'))
    return [id for id in banner_ids if id not in exclude_banner_ids]


def get_topX_unique_banners_with_revenue_totals(x, campaign, quarter, banners_seen):
    key = '%s-%s-%s' % (settings.REDIS_PREFIX_TOP10_BY_REVENUE, campaign, quarter)
    banner_ids = json.loads(r.get(key).decode('utf-8'))

    return [id for id in banner_ids if id not in banners_seen][:x]


def fill_redis():
    r.flushdb()
    for quarter in range(1, 5):
        # unique with revenue
        for campaign in models.Campaign.objects.all():
            banner_ids_qs = models.Click.objects \
                .filter(campaign=campaign, quarter=quarter, conversions__revenue__gt=0) \
                .values('banner_id') \
                .distinct()

            key = '%s-%s-%s' % (settings.REDIS_PREFIX_UNIQUE_WITH_REVENUE, campaign, quarter)
            banner_ids = [b['banner_id'] for b in banner_ids_qs]
            r.set(key, json.dumps(banner_ids))

        # top 10 by revenue
        banner_ids_qs = models.Click.objects.filter(banner_id__in=banner_ids) \
            .values('banner_id') \
            .distinct() \
            .order_by('-conversion_revenue_sum') \
            .values('banner_id').distinct()[:10]

        key = '%s-%s-%s' % (settings.REDIS_PREFIX_TOP10_BY_REVENUE, campaign, quarter)
        top10_banner_ids = [b['banner_id'] for b in banner_ids_qs]
        r.set(key, json.dumps(top10_banner_ids))

    # random
    random_qs = models.Banner.objects.all() \
        .order_by('?') \
        .values('banner_id')[:10]

    key = '%s' % settings.REDIS_PREFIX_RANDOM_BANNERS
    random_banner_ids = [b['banner_id'] for b in random_qs]
    r.set(key, json.dumps(random_banner_ids))

    # by number of clicks
    top10_by_clicks_qs = models.Banner.objects.all() \
        .annotate(count=Count('clicks')) \
        .filter(count__gt=0) \
        .order_by('-count') \
        .values('banner_id') \
        .distinct()[:10]

    key = '%s' % settings.REDIS_PREFIX_TOP10_BY_CLICKS
    top10_by_clicks_banner_ids = [b['banner_id'] for b in top10_by_clicks_qs]
    r.set(key, json.dumps(top10_by_clicks_banner_ids))
