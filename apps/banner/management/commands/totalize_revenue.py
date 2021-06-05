from django.core.management.base import BaseCommand
from django.db.models import Sum

from apps.banner import models


class Command(BaseCommand):
    help = """
    Aggregate revenue in clicks model
    """

    def handle(self, *args, **options):
        for click in models.Click.objects.all().annotate(total=Sum('conversions')):
            if click.total:
                click.conversion_revenue_sum = click.total
            else:
                click.conversion_revenue_sum = 0
