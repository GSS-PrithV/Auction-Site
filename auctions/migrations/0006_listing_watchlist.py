# Generated by Django 4.0.4 on 2022-07-27 19:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_comment_bids'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
