# Generated by Django 3.1.6 on 2021-06-05 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0009_click_quarter'),
    ]

    operations = [
        migrations.AddField(
            model_name='click',
            name='conversion_revenue_sum',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=10),
        ),
    ]
