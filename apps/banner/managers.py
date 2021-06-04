from django.db.models import Manager, Sum


class ClickManager(Manager):
    def get_unique_banners_with_revenue(self, campaign, quarter, banners_seen):
        return self.get_queryset() \
            .filter(campaign=campaign, quarter=quarter, conversions__revenue__gt=0) \
            .exclude(banner_id__in=banners_seen) \
            .values('banner_id').distinct()

    def get_top10_unique_banners_with_revenue_totals(self, campaign, quarter, banners_seen):
        return self.get_queryset() \
            .filter(campaign=campaign, quarter=quarter, conversions__revenue__gt=0) \
            .exclude(banner_id__in=banners_seen) \
            .values('banner_id').distinct() \
            .annotate(total_revenue=Sum('conversions__revenue')) \
            .order_by('total_revenue') \
            .values_list('banner_id', flat=True)[:10]
