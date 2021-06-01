import json
from io import StringIO
import os

import django
from django.conf import settings
from django.core import management

from locust import HttpLocust, TaskSet

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

django.setup()

out = StringIO()
management.call_command(
    'show_urls',
    format='json',
    stdout=out
)

patterns = json.loads(out.getvalue())

headers = {
    'User-Agent': 'datachef'
}


def factory(path):
    def _locust(locust):
        locust.client.get(path, headers=headers)
    return _locust


alltasks = {factory(pattern['url']): 1 for pattern in patterns if '-list' in pattern['name']}


class UserBehavior(TaskSet):
    tasks = alltasks


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 5000
