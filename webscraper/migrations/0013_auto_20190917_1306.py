# Generated by Django 2.2.5 on 2019-09-17 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webscraper', '0012_auto_20190917_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrape',
            name='endTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='last_update_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='scrape',
            name='startTime',
            field=models.DateTimeField(),
        ),
    ]
