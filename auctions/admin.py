from django.contrib import admin

from .models import User, Listing, Bid, Comment, Category

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "listing_user","__str__", "image_url")

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
