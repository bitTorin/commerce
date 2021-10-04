from django.contrib.auth.models import AbstractUser
from djmoney.models.fields import MoneyField
from django.db import models



class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)

class Bid(models.Model):
    price = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11,)

class Comment(models.Model):
    comment = models.CharField(max_length=500, default='Enter Comment Here')
