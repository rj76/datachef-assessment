from django.core.management.base import BaseCommand

from apps.banner.utils import aggregate_revenue


class Command(BaseCommand):
    help = """
    Aggregate revenue in clicks model
    """

    def handle(self, *args, **options):
        aggregate_revenue()
