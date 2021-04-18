from django.contrib.auth.models import AbstractUser
from django.db import models


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
    category = models.IntegerField(max_length=64, choices=categories, blank=True)

    def __str__(self):
        return f"{self.name}"


class WatchedItem(models.Model):
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# class Comments(models.Model):
#     listing_name = models.ForeignKey(AuctionListings.name, on_delete=models.CASCADE)
#     user_name = models.ForeignKey(User.username, on_delete=models.CASCADE)
#     comment = models.CharField(max_length=280)
#     time = models.DateTimeField()
