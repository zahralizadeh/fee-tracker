# Generated by Django 2.2.5 on 2019-09-14 07:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('webscraper', '0006_auto_20190913_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrape',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 14, 7, 14, 30, 609594, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 14, 7, 14, 30, 609541, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='status',
            field=models.CharField(default='initialied', max_length=20),
        ),
    ]
