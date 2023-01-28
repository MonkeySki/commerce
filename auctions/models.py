from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    amount = models.IntegerField(default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"${self.amount}"
    

class Listing(models.Model):
    CATEGORIES = ['Electronics', 'Home', 'Fashion', 'Toys', 'Other']
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    bids = models.ForeignKey(Bid, on_delete=models.CASCADE, null=True)
    image = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    dateListed = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions",null=True )
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won", null=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title}"


class Comments(models.Model):
    comment = models.CharField(max_length=64)
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", null=True)

    def __str__(self):
        return f"{self.comment} by {self.commentor}"






