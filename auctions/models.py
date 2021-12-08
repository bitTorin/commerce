from django.contrib.auth.models import AbstractUser
from djmoney.models.fields import MoneyField
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    category = models.ForeignKey('Category', to_field='slug', on_delete=models.CASCADE, null=True, related_name="category")
    listing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_user", default=User)
    image_url = models.URLField()
    starting_bid = models.ForeignKey('Bid', on_delete=models.CASCADE, null=True, related_name='+')
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    price = MoneyField(decimal_places=2, default=0.00, default_currency='USD', max_digits=11,)
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.price}"

class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=500, default='Enter Comment Here')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")

    def __str__(self):
        return f"{self.item} : {self.user}- '{self.text}'"

class Watchlist(models.Model):
    user_watchlist = models.ForeignKey(User, on_delete=models.CASCADE)
    watchlist_items = models.ManyToManyField(Listing, blank=True)

    def __str__(self):
        return f"{self.user_watchlist}"
