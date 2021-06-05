from django.db.models import Manager, Count


class BannerManager(Manager):
    def get_random_banner_ids(self, count, exclude_banner_ids):
        return self.get_queryset() \
            .exclude(banner_id__in=exclude_banner_ids) \
            .order_by('?') \
            .values_list('banner_id', flat=True)[:count]

    def get_banner_ids_by_click_count(self, exclude_banner_ids):
        return self.get_queryset() \
            .exclude(banner_id__in=exclude_banner_ids) \
            .annotate(count=Count('clicks')) \
            .filter(count__gt=0) \
            .order_by('-count') \
            .values_list('banner_id', flat=True)


class ClickManager(Manager):
    def get_unique_banners_with_revenue(self, campaign, quarter, banners_seen):
        return self.get_queryset() \
            .filter(campaign=campaign, quarter=quarter, conversion_revenue_sum__gt=0) \
            .exclude(banner_id__in=banners_seen) \
            .values('banner_id').distinct()

    def get_top10_unique_banners_with_revenue_totals(self, campaign, quarter, banners_seen):
        return self.get_queryset() \
            .filter(campaign=campaign, quarter=quarter, conversion_revenue_sum__gt=0) \
            .exclude(banner_id__in=banners_seen) \
            .values('banner_id').distinct() \
            .order_by('-conversion_revenue_sum') \
            .values_list('banner_id', flat=True)[:10]

    def get_x_unique_banners_with_revenue_totals(self, campaign, quarter, banners_seen, x):
        return self.get_queryset() \
                   .filter(campaign=campaign, quarter=quarter, conversion_revenue_sum__gt=0) \
                   .exclude(banner_id__in=banners_seen) \
                   .order_by('-conversion_revenue_sum') \
                   .values_list('banner_id', flat=True).distinct()[:x]
