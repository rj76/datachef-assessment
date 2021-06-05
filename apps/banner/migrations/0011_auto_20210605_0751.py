# Generated by Django 3.1.6 on 2021-06-05 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0010_click_conversion_revenue_sum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='click',
            name='conversion_revenue_sum',
            field=models.DecimalField(db_index=True, decimal_places=8, default=0, max_digits=10),
        ),
    ]
