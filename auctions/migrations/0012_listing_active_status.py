# Generated by Django 3.2.7 on 2021-12-08 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_listing_starting_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='active_status',
            field=models.BooleanField(default=True),
        ),
    ]