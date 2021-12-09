from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from django.db.models import Max
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from .models import User, Listing, Bid, Comment, Category, Watchlist

class NewListingForm(forms.Form):
    title = forms.CharField(label="title")
    description = forms.CharField(label="description")
    category = forms.CharField(label="category")
    image_url = forms.URLField(label="image_url")
    starting_bid = forms.DecimalField(max_digits=11, decimal_places=2, label="starting_bid")

class WatchlistForm(forms.Form):
    listing_title = forms.CharField(label="listing_title")

class CommentForm(forms.Form):
    comment_text = forms.CharField(label="comment_text")

    class Meta:
        model = Comment
        fields = ('text',)

class NewBidForm(forms.Form):
    bid_price = forms.DecimalField(max_digits=11, decimal_places=2, label="bid_price")

    class Meta:
        model = Bid
        fields = ('price',)

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        # "bids": Bid.objects.all(),
        # "top_bid": Listing.objects.filter(bids).order_by('-price')[0],
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

            bid = Bid()
            bid.price = form.cleaned_data["starting_bid"]
            bid.listing = Listing.objects.get(pk=listing_id)
            bid.bid_user = request.user
            bid.save()

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
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        user = "null"

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "title": listing.title,
        "comments": listing.comments.all(),
        "listing_user": listing.listing_user,
        "image_url": listing.image_url,
        "description": listing.description,
        "watchlist": Watchlist.objects.all(),
        "bids":Bid.objects.filter(listing = listing).order_by('-price').all(),
        "top_bid":Bid.objects.filter(listing = listing).order_by('-price')[0],
        "user": user,
    })


@login_required
def watchlist(request):
    user_id = request.user.pk
    user_list = Watchlist.objects.get(user_watchlist=user_id)
    watch_items = user_list.watchlist_items.all()
    return render(request, "auctions/watchlist.html", {
        "listings": watch_items.all()
    })


@login_required
def watchlist_add(request, listing_id):
    if request.method == "POST":
        try:
            add_listing = Listing.objects.get(pk=listing_id)
        except KeyError:
            return HttpResponseBadRequest("Bad Request: no listing chosen")
        except Listing.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: listing does not exist")
        if Watchlist.objects.filter(user_watchlist = request.user, watchlist_items = listing_id).exists():
            messages.add_message(request, messages.ERROR, "Item already in watchlist")
            return HttpResponseRedirect(reverse("watchlist"))
        else:
            user_list, created = Watchlist.objects.get_or_create(user_watchlist = request.user)
            user_list.watchlist_items.add(add_listing)
            return HttpResponseRedirect(reverse("watchlist"))


@login_required
def watchlist_remove(request, listing_id):
    if request.method == "POST":
        remove_listing = get_object_or_404(Listing, pk=listing_id)
        user_list = Watchlist.objects.get(user_watchlist = request.user)
        user_list.watchlist_items.remove(remove_listing)
        return HttpResponseRedirect(reverse("watchlist"))

@login_required
def place_bid(request, listing_id):
    if request.method == "POST":
        form = NewBidForm(request.POST)
        if form.is_valid():
            bid = Bid()
            bid.price = form.cleaned_data["bid_price"]
            bid.listing = Listing.objects.get(pk=listing_id)
            bid.bid_user = request.user
            top_bid = Bid.objects.filter(listing = bid.listing).order_by('-price').first()
            listing_user = bid.listing.listing_user
            if bid.bid_user is not listing_user:
                if top_bid.bid_user is not listing_user:
                    if bid.price > top_bid.price:
                        bid.save()
                        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
                    else:
                        return HttpResponse("Bid amount too low. Please try again.")
                else:
                    if bid.price >= top_bid.price:
                        bid.save()
                        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
                    else:
                        return HttpResponse("Bid amount too low. Please try again.")
            else:
                return HttpResponse("You may not bid on your own auction.")


    else:
        form = NewBidForm()

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def accept_bid(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    listing_user = listing.listing_user
    if user == listing_user:
        bid = Bid()
        bid.listing = Listing.objects.get(pk=listing_id)
        winning_bid = Bid.objects.filter(listing = bid.listing).order_by('-price').first()
        listing.active_status = False
        listing.save()

        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        pass

@login_required
def comment(request, listing_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.text = form.cleaned_data["comment_text"]
            comment.item = Listing.objects.get(pk=listing_id)
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        form = CommentForm()

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def category(request, slug):
    category_list = Category.objects.all()
    
    if slug == 'all':
        listings = Listing.objects.all()
        return render(request, "auctions/category.html", {
            "categories": category_list,
            "listings": listings
        })

    else:
        input_slug = slug
        cat = Category.objects.get(slug=input_slug)
        listings = Listing.objects.all().filter(category = cat)
        return render(request, "auctions/category.html", {
            "categories": category_list,
            "listings": listings,
        })
