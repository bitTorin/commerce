# Generated by Django 3.2.9 on 2021-12-13 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_top_bid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='top_bid',
            new_name='bids',
        ),
    ]