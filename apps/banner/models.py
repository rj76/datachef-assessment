from django.db import models


class Banner(models.Model):
    banner_id = models.PositiveIntegerField(primary_key=True, unique=True)

    objects = models.Manager()


class Campaign(models.Model):
    campaign_id = models.PositiveIntegerField(primary_key=True, unique=True)

    objects = models.Manager()


class Impression(models.Model):
    quarter = models.PositiveSmallIntegerField(db_index=True)
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE, related_name='impressions')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='impressions')

    class Meta:
        unique_together = ('quarter', 'banner', 'campaign')

    objects = models.Manager()


class Click(models.Model):
    click_id = models.PositiveIntegerField(primary_key=True, unique=True)
    impression = models.ForeignKey(Impression, on_delete=models.CASCADE, related_name='clicks')

    class Meta:
        unique_together = ('click_id', 'impression')

    objects = models.Manager()


class Conversion(models.Model):
    conversion_id = models.PositiveIntegerField(primary_key=True, unique=True)
    click = models.ForeignKey(Click, on_delete=models.CASCADE, related_name='conversions')
    revenue = models.DecimalField(max_digits=10, decimal_places=8)

    objects = models.Manager()
