import csv
import logging

from django.conf import settings

from apps.banner import models

logger = logging.getLogger('apps.banner')


class Batch:
    def import_all(self):
        for quarter in range(1, 5):
            self.import_impressions(quarter)
            self.import_clicks(quarter)
            self.import_conversions(quarter)

    def import_impressions(self, quarter):
        file = '%s/data/%d/impressions_%d.csv' % (settings.BASE_DIR, quarter, quarter)
        num_exist = 0

        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            for row in reader:
                as_dict = dict(zip(headers, row))
                banner, _ = models.Banner.objects.get_or_create(
                    banner_id=as_dict['banner_id']
                )

                campaign, _ = models.Campaign.objects.get_or_create(
                    campaign_id=as_dict['campaign_id']
                )

                _, created = models.Impression.objects.get_or_create(
                    quarter=quarter,
                    banner=banner,
                    campaign=campaign
                )

                if not created:
                    num_exist += 1
                    logger.debug('impression with banner_id %s and campaign_id %s already exists'
                                 % (as_dict['banner_id'], as_dict['campaign_id']))

        logger.info('%d double impressions' % num_exist)

    def import_clicks(self, quarter):
        file = '%s/data/%d/clicks_%d.csv' % (settings.BASE_DIR, quarter, quarter)

        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            for row in reader:
                as_dict = dict(zip(headers, row))
                banner = models.Banner.objects.get(banner_id=as_dict['banner_id'])
                campaign = models.Campaign.objects.get(campaign_id=as_dict['campaign_id'])

                impression = models.Impression.objects.get(
                    quarter=quarter,
                    banner=banner,
                    campaign=campaign
                )

                models.Click.objects.get_or_create(
                    click_id=as_dict['click_id'],
                    impression=impression
                )

    def import_conversions(self, quarter):
        file = '%s/data/%d/conversions_%d.csv' % (settings.BASE_DIR, quarter, quarter)

        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            for row in reader:
                as_dict = dict(zip(headers, row))
                click = models.Click.objects.get(click_id=as_dict['click_id'])

                conversion, _ = models.Conversion.objects.get_or_create(
                    conversion_id=as_dict['conversion_id'],
                    click=click,
                    revenue=float(as_dict['revenue'])
                )
