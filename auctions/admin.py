from django.contrib import admin

from .models import User, Listing, Bid, Comment, Category, Watchlist

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "listing_user","__str__", "description", "image_url")

class WatchlistAdmin(admin.ModelAdmin):
    filter_horizontal = ("watchlist_items",)

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Watchlist, WatchlistAdmin)
