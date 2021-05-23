
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    categories = (
        (1, "Fashion"),
        (2, "Toys"),
        (3, "Homeware"),
        (4, "Electronics"),
    )
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=280)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=8)
    image = models.URLField(blank=True)
    category = models.IntegerField(choices=categories, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=3)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class Bid(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=8)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = "created_at"

    def __str__(self):
        return f"{self.amount}"


class WatchedItem(models.Model):
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auction_listing}"


class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=280)
    time = models.DateTimeField(auto_now_add=True)
