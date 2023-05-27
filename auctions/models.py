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

    def __str__(self):
        return self.title


class user_watchList(models.Model):
    ownerWatchList = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='watchlists')
    idNumber = models.IntegerField()
    listnaem = 'bengo'

    def __str__(self):
        return self.listnaem


class bids(models.Model):
    bidsa = models.FloatField(max_length=10)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="bids")
    listname = models.ForeignKey(
        Listing, on_delete=models.CASCADE, blank=True, null=True)
    ListID = models.IntegerField(max_length=10)

    def __str__(self):
        return str(self.bidsa)


class comments(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True, related_name='comments_user_id')
    list_ID = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False, null=True, related_name='comments_list_id')
    comment = models.CharField(max_length=300)
