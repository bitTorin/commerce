from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("category", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/watchlist_add", views.watchlist_add, name="watchlist_add"),
    path("<int:listing_id>/watchlist_remove", views.watchlist_remove, name="watchlist_remove"),
    path("<int:listing_id>/place_bid", views.place_bid, name="place_bid"),
    path("<int:listing_id>/accept_bid", views.accept_bid, name="accept_bid")
]
