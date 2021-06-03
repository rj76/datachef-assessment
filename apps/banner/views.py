from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import utils


class HomeView(TemplateView):
    template_name = "banner/index.html"


class CampaignDetail(APIView):
    def get(self, request, *args, **kwargs):
        campaign = get_object_or_404(models.Campaign, pk=kwargs['pk'])
        quarter = utils.get_current_quarter()
        client_ip = request.META['REMOTE_ADDR']

        # we could also exclude more banners
        # (e.g. per day, but we'll just exclude the last one seen)
        last_banner_seen = models.BannerSeen.objects.filter(address=client_ip) \
            .order_by('-datetime') \
            .first()

        if not last_banner_seen:
            last_banner_seen = []
        else:
            last_banner_seen = [last_banner_seen.banner_id]

        banner_ids = models.Click.objects \
            .filter(impression__campaign=campaign, impression__quarter=quarter) \
            .exclude(impression__banner_id__in=last_banner_seen) \
            .annotate(total_revenue=Sum('conversions__revenue')) \
            .order_by('total_revenue') \
            .values_list('impression__banner_id', flat=True)[:5]

        for banner_id in banner_ids:
            models.BannerSeen.objects.create(
                banner_id=banner_id,
                address=client_ip
            )

        return Response(banner_ids)
