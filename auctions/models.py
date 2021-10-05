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
    user_listing = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listing")

    def __str__(self):
        return f"{self.title} : {self.description}"

class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    price = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11,)
    user_bid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")

    def __str__(self):
        return f"{self.user_bid} : {self.item} : {self.price}"

class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=500, default='Enter Comment Here')
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")

    def __str__(self):
        return f"{self.item} : {self.user_comment}- '{self.comment}'"
