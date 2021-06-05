import os
import django
from locust import HttpUser, task, between

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()


class User(HttpUser):
    # host = 'http://127.0.0.1:9000'
    host = 'https://datachef.pedroja.tech'
    def on_start(self):
        """ Run on start for every Locust hatched """
        self.client.headers['Referer'] = self.client.base_url
        self.client.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (' \
                                            'KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36 '

    def get_campaign_pks(self):
        from apps.banner import models

        return [c.campaign_id for c in models.Campaign.objects.all().order_by('?')[:50]]

    @task(1)
    def get_campaigns(self):
        for campaign_id in self.get_campaign_pks():
            self.client.get('/campaign/%d/' % campaign_id)
