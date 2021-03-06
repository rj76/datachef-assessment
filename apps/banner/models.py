from django.db import models

from . import managers


class Banner(models.Model):
    banner_id = models.PositiveIntegerField(primary_key=True, unique=True)

    objects = managers.BannerManager()


class Campaign(models.Model):
    campaign_id = models.PositiveIntegerField(primary_key=True, unique=True)

    objects = models.Manager()


class Impression(models.Model):
    quarter = models.PositiveSmallIntegerField(db_index=True)
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE, related_name='impressions')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='impressions')

    objects = models.Manager()


class Click(models.Model):
    click_id = models.PositiveIntegerField(primary_key=True, unique=True)
    quarter = models.PositiveSmallIntegerField(db_index=True, null=True)
    num_impressions = models.PositiveIntegerField(default=0)
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE, related_name='clicks', null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='clicks', null=True)
    conversion_revenue_sum = models.DecimalField(max_digits=20, decimal_places=8, default=0, db_index=True)

    objects = managers.ClickManager()


class Conversion(models.Model):
    conversion_id = models.PositiveIntegerField(primary_key=True, unique=True)
    click = models.ForeignKey(Click, on_delete=models.CASCADE, related_name='conversions')
    revenue = models.DecimalField(max_digits=10, decimal_places=8)

    objects = models.Manager()


class BannerSeen(models.Model):
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE, related_name='ips', db_index=True)
    address = models.CharField(max_length=50, db_index=True)
