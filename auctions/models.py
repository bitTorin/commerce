from django.contrib.auth.models import AbstractUser
from djmoney.models.fields import MoneyField
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    listing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_user", default=User)
    image_url = models.URLField()

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    price = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11,)
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")

    def __str__(self):
        return f"{self.bid_user} : {self.item} : {self.price}"

class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=500, default='Enter Comment Here')
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")

    def __str__(self):
        return f"{self.item} : {self.comment_user}- '{self.comment}'"

class Watchlist(models.Model):
    user_watchlist = models.ForeignKey(User, on_delete=models.CASCADE)
    watchlist_items = models.ManyToManyField(Listing, blank=True)

    def __str__(self):
        return f"{self.user_watchlist}"
