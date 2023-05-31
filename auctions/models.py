from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Catagory(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName


class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    imageUrl = models.CharField(max_length=1000)
    price = models.FloatField()
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="listings")
    category = models.ForeignKey(
        Catagory, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    created_at = models.DateTimeField(auto_now_add=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")

    def __str__(self):
        return self.title

class bids(models.Model):
    bidsa = models.FloatField(max_length=10, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="bids")
    listname = models.ForeignKey(
        Listing, on_delete=models.CASCADE, blank=True, null=True)
    ListID = models.IntegerField(max_length=10)

    def __str__(self):
        return f"bid {self.bidsa} | user {self.owner} | list {self.listname} | list id {self.ListID}"

class user_watchList(models.Model):
    ownerWatchList = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='watchlists')
    idNumber = models.IntegerField()

    def __str__(self):
        return f" LIST for {self.ownerWatchList} {self.idNumber} "




class comments(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE,
                                blank=False, null=True, related_name='comments_user_id')
    list_ID = models.ForeignKey(Listing, on_delete=models.CASCADE,
                                blank=False, null=True, related_name='comments_list_id')
    comment = models.CharField(max_length=300)

    def __str__(self) -> str:
        return f"  comment on {self.list_ID} BY {self.user_ID}"
