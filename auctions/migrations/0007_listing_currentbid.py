# Generated by Django 4.0.4 on 2022-07-27 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listing_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='CurrentBid',
            field=models.IntegerField(default=0),
        ),
    ]