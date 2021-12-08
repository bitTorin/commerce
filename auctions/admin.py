from django.contrib import admin

from .models import User, Listing, Bid, Comment, Category, Watchlist

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "active_status", "listing_user", "starting_bid", "__str__", "description", "image_url")
    filter_horizontal = ("category",)

class WatchlistAdmin(admin.ModelAdmin):
    filter_horizontal = ("watchlist_items",)

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "bid_user", "listing")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "user", "text")

class CategoryAdmin(admin.ModelAdmin):
    filter_horizontal = ("listings",)

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
