from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment, Category, Watchlist

class NewListingForm(forms.Form):
    title = forms.CharField(label="title")
    description = forms.CharField(label="description")
    category = forms.CharField(label="category")
    image_url = forms.URLField(label="image_url")

class WatchlistForm(forms.Form):
    listing_title = forms.CharField(label="listing_title")

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            listing = Listing()
            listing.title = form.cleaned_data["title"]
            listing.description = form.cleaned_data["description"]
            listing.image_url = form.cleaned_data["image_url"]
            listing.category = Category.objects.get(name = (request.POST["category"]))
            listing.listing_user = User.objects.get(username = request.user.username)

            listing.save()
            listing_id = listing.id

            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    else:
        return render(request, "auctions/create.html", {
            "categories": Category.objects.all()
        })


def listing(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "title": listing.title,
        "bids": listing.bids.all(),
        "comments": listing.comments.all(),
        # "category": listing.category(),
        "listing_user": listing.listing_user,
        "image_url": listing.image_url,
        "description": listing.description,
    })


@login_required
def watchlist(request, user):
    return render(request, "auctions/watchlist.html", {
        "user": user,
        "title": listing.title,
        "description": listing.description,
        "image_url": listing.image_url,
    })


@login_required
def watchlist_add(request, listing_id):
    # add_listing = get_object_or_404(Listing, pk=listing_id)
    # obj, created = Watchlist.objects.get_or_create(user=request.user, id=listing_id)
    #
    # if Watchlist.objects.filter(user = request.user, listing = listing_id).exists():
    #     messages.add_message(request, messages.ERROR, "Item already in watchlist")
    #     return HttpResponseRedirect(reverse("index"))
    #
    # user_list, created = Watchlist.objects.get_or_create(user=request.user)
    #
    # user_list.listing.add(add_listing)
    # messages.add_message(request, messages.SUCCESS, "Item added to watchlist")
    # return render(request, "auctions/watchlist.html", {
    #     "user" = request.user.username
    # })

    # Revision

    try:
        # user_list = Watchlist.objects.get(user = request.user.username, id = listing_id)
        # user_list = Watchlist.objects.get(user = request.user.username)
        listing = Listing.objects.get(pk=listing_id)
        user_list = Watchlist.objects.get(user = request.user.username, id = listing_id)
    except KeyError:
        return HttpResponseBadRequest("Bad Request: no listing chosen")
    except Listing.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: listing does not exist")
    
    if Watchlist.objects.filter(user = user, listing = listing_id).exists():
        messages.add_message(request, messages.ERROR, "Item already in watchlist")
        return HttpResponseRedirect(reverse("listing", listing_id))
    else:
        user_list.listing.add(listing)
        return HttpResponseRedirect(reverse("watchlist", user))


@login_required
def watchlist_remove(request, listing_id):
    remove_listing = get_object_or_404(Listing, pk=listing_id)
    watchlistings = Watchlist.objects.all()

    watchlistings.listing.remove(remove_listing)
    return render (request, "auctions/watchlist.html")


def category(request):
    return render(request, "auctions/category.html", {
        "categories": Category.objects.all()
    })
