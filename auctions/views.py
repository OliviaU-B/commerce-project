from importlib._common import _

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .models import User, AuctionListing, WatchedItem, Bid, Comment
from .forms import NewListingForm


def index(request):
    auctions = AuctionListing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "auctions": auctions,
    })


def categories(request):
    categories = AuctionListing.categories
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })


def view_category(request, category):
    auctions = AuctionListing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/view_category.html", {
        "category": category,
        "auctions": auctions,
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



def create_new_listing(request):
    if request.method == 'POST':
        AuctionListing.objects.create(name=request.POST["listing_name"],
                                      description=request.POST["description"],
                                      starting_bid=request.POST["starting_bid"],
                                      image=request.POST["image"],
                                      category=int(request.POST["category"]))

    return render(request, "auctions/create_new_listing.html", {'form': NewListingForm})


def view_listing(request, id):
    listing = AuctionListing.objects.get(id=id)
    is_active = listing.is_active
    highest_bidder = None
    is_owner = False
    is_watched = False
    if request.user == listing.created_by:
        is_owner = True
    if len(Bid.objects.filter(auction_listing=listing)):
        highest_bid = Bid.objects.filter(auction_listing=listing).latest('created_at')
        highest_bidder = User(id=highest_bid.bidder_id)
    if request.user.is_authenticated:
        is_watched = WatchedItem.objects.filter(auction_listing=listing,
                                                user=request.user)
    current_user = request.user

    comments = Comment.objects.filter(listing=id)
    if request.method == 'POST':
        Comment.objects.create(listing=listing,
                               user=request.user,
                               comment_text=request.POST["comment_text"])
        HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watched": is_watched,
        "comments": comments,
        "is_owner": is_owner,
        "is_active": is_active,
        "highest_bidder": highest_bidder,
        "current_user": current_user,
    })


def close_listing(request, id):
    listing = AuctionListing.objects.get(id=id)
    if listing.created_by == request.user:
        listing.is_active=False
        listing.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="login")
def add_to_watchlist(request, id):
    listing = AuctionListing.objects.get(id=id)
    WatchedItem.objects.create(auction_listing=listing,
                               user=request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="login")
def remove_from_watchlist(request, id):
    listing = AuctionListing.objects.get(id=id)
    WatchedItem.objects.filter(auction_listing=listing,
                               user=request.user).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="login")
def view_watchlist(request):
    watched_items = WatchedItem.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "watched_items": watched_items,
    })


@login_required(login_url="login")
def place_bid(request, id):
    listing = AuctionListing.objects.get(id=id)
    bid = float(request.POST["bid_amount"])
    bids = Bid.objects.filter(auction_listing=listing)
    if len(bids) != 0:
        current_bid = Bid.objects.filter(auction_listing=listing).latest('created_at')
        if bid > current_bid.amount:
            Bid.objects.create(amount=bid,
                               bidder=request.user,
                               auction_listing=listing)
        else:
            raise ValidationError(_("Bid too low"))
    else:
        starting_bid = listing.starting_bid
        if bid > starting_bid:
            Bid.objects.create(amount=bid,
                               bidder=request.user,
                               auction_listing=listing)
        else:
            raise ValidationError(_("Bid too low"))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))