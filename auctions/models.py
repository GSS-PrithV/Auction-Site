from distutils.command.upload import upload
from time import time
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.category

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bid_Owner")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="Bid_Category")
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    StartingBid = models.IntegerField()
    CurrentBid = models.IntegerField(default=0)
    Thumbnail = models.URLField(blank = True, null = True)
    postTime = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")

class Bids(models.Model):
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_item")

    def __str__(self):
        return f"Bid {self.id} by {self.user} for {self.amount} on {self.auction}"

class Comment(models.Model):
    comment = models.TextField(max_length=300)
    time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor")
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commentor")


