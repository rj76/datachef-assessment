import csv
import logging

from django.conf import settings

from apps.banner import models

logger = logging.getLogger('apps.banner')


class Batch:
    test = False

    def import_all(self, test=False):
        if test:
            self.test = True
            self.import_impressions(1)
            self.import_clicks(1)
            self.import_conversions(1)

            return

        for quarter in range(1, 5):
            self.import_impressions(quarter)
            self.import_clicks(quarter)
            self.import_conversions(quarter)

    def import_impressions(self, quarter):
        file = '%s/data/test/impressions.csv' % settings.BASE_DIR if self.test else '%s/data/%d/impressions_%d.csv' % (
            settings.BASE_DIR, quarter, quarter)

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

                models.Impression.objects.create(
                    quarter=quarter,
                    banner=banner,
                    campaign=campaign
                )

    def import_clicks(self, quarter):
        file = '%s/data/test/clicks.csv' % settings.BASE_DIR if self.test else '%s/data/%d/clicks_%d.csv' % (
            settings.BASE_DIR, quarter, quarter)
        num_exist = 0

        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            for row in reader:
                as_dict = dict(zip(headers, row))
                banner = models.Banner.objects.get(banner_id=as_dict['banner_id'])
                campaign = models.Campaign.objects.get(campaign_id=as_dict['campaign_id'])

                num_impressions = models.Impression.objects.filter(
                    quarter=quarter,
                    banner=banner,
                    campaign=campaign
                ).count()

                try:
                    click = models.Click.objects.get(click_id=as_dict['click_id'])
                    click.quarter = quarter
                    click.num_impressions = num_impressions
                    click.banner = banner
                    click.campaign = campaign
                    click.save()

                    num_exist += 1
                    logger.debug('duplicate click_id: %s' % as_dict['click_id'])
                except models.Click.DoesNotExist:
                    models.Click.objects.create(
                        click_id=as_dict['click_id'],
                        quarter=quarter,
                        num_impressions=num_impressions,
                        banner=banner,
                        campaign=campaign,
                    )

        logger.info('%d duplicate clicks' % num_exist)

    def import_conversions(self, quarter):
        file = '%s/data/test/conversions.csv' % settings.BASE_DIR if self.test else '%s/data/%d/conversions_%d.csv' % (
            settings.BASE_DIR, quarter, quarter)
        num_exist = 0

        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            for row in reader:
                as_dict = dict(zip(headers, row))
                click = models.Click.objects.get(click_id=as_dict['click_id'])

                try:
                    conversion = models.Conversion.objects.get(conversion_id=as_dict['conversion_id'])
                    conversion.click = click
                    conversion.revenue = float(as_dict['revenue'])
                    conversion.save()

                    num_exist += 1
                    logger.debug('duplicate conversion_id: %s' % as_dict['conversion_id'])
                except models.Conversion.DoesNotExist:
                    models.Conversion.objects.create(
                        conversion_id=as_dict['conversion_id'],
                        click=click,
                        revenue=float(as_dict['revenue'])
                    )

        logger.info('%d duplicate conversions' % num_exist)
