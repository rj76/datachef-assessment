# Generated by Django 3.1.6 on 2021-06-04 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0005_auto_20210604_0639'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='click',
            unique_together=set(),
        ),
    ]