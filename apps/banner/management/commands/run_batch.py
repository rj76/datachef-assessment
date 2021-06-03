from django.core.management.base import BaseCommand

from apps.banner.batch import Batch


class Command(BaseCommand):
    help = """
    Import datasets
    """

    def handle(self, *args, **options):
        batch = Batch()
        batch.import_all()
