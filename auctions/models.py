from django.contrib.auth.models import AbstractUser
from djmoney.models.fields import MoneyField
from django.db import models



class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.title} : {self.description}"

class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    price = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11,)

    def __str__(self):
        return f"{self.item} : {self.price}"

class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=500, default='Enter Comment Here')

    def __str__(self):
        return f"{self.item} : {self.comment}"
