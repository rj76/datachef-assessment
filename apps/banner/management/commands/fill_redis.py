from django.core.management.base import BaseCommand

from apps.banner import redis


class Command(BaseCommand):
    help = """
    Fill redis with database content
    """

    def handle(self, *args, **options):
        redis.fill_redis()
