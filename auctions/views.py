from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comments


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True)
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

def NewListing(request):
    if request.method == "POST":
        newBid = Bid()
        newBid.amount = request.POST['startingBid']
        newBid.save()

        newListing = Listing()
        newListing.title = request.POST['title']
        newListing.description = request.POST['description']
        newListing.bids = newBid
        newListing.image = request.POST['image']
        newListing.category = request.POST['category']
        newListing.owner = request.user
        newListing.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        categories = Listing.CATEGORIES
        return render(request, "auctions/NewListing.html", {
            "categories": categories,
        })

def ListingPage(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = User.objects.get(username=request.user)

    if request.method == "POST":
        comment = Comments()
        comment.comment = request.POST['comment']
        comment.commentor = user
        comment.listing = listing
        comment.save()

    return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": listing.comments.all(),
            "watchers": listing.watchers.all()
        })

def watchlist(request):
    user = User.objects.get(username=request.user)
    if request.method == "POST":
        listing_id = request.POST['listing']
        listing = Listing.objects.get(id=listing_id)
        if request.POST['action'] == 'Add to Watchlist':
            listing.watchers.add(user)
            listing.save()
        elif request.POST['action'] == 'Remove from Watchlist':
            listing.watchers.remove(user)
            listing.save()
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": listing.comments.all(),
            "watchers": listing.watchers.all()
        })              
    
    else:
        return render(request, "auctions/watchlist.html", {
            "listings": user.watchlist.all()
        })

def categories(request):
    categories = Listing.CATEGORIES
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })

def category(request, category):
    listings = Listing.objects.filter(category=category, active=True)
    return render(request, "auctions/categoryListings.html", {
        "listings": listings,
        "category": category
    })

def closeAuction(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.winner = listing.bids.bidder
    listing.active = False
    listing.save()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": listing.comments.all(),
        "watchers": listing.watchers.all()
    })

def bid(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if int(request.POST['bid']) > listing.bids.amount:
        user = User.objects.get(username=request.user)
        newBid = Bid()
        newBid.amount = int(request.POST['bid'])
        newBid.bidder = user
        newBid.save()

        listing.bids = newBid
        listing.save()

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": listing.comments.all(),
            "watchers": listing.watchers.all()
        })
    else:
        return HttpResponse("Bid not high enough")
