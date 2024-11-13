from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from decimal import Decimal

from .models import User,Auction_listings,Category,Watchlist,Bids,Comments


def index(request):
    listings=Auction_listings.objects.filter(is_active=True)
    return render(request, "auctions/index.html",{
        "listings":listings,
        "heading":"Active Listing"
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
                "message": "Invalid username and/or password.",
            })
    else:
        return render(request, "auctions/login.html",{
            
        })


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
                "message": "Passwords must match.",
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
def create(request):
    owner=request.user
    if request.method=="GET":
        return render(request,"auctions/create.html",{
            "owner":owner,
            "cars":Category.objects.all(),
            "categories":Category.objects.all()
        })
    else:
        title=request.POST['title']
        description=request.POST['description']
        imgurl=request.POST['imgurl']
        stbid=request.POST['stbid']
        category=request.POST['category']
        category_instance = get_object_or_404(Category, name=category)
        stbid_clean = stbid.replace('$', '').strip()
        bid = Bids(bid=stbid_clean,user=owner)
        bid.save()
        newlisting=Auction_listings(title=title, Owner=owner, description=description, imgurl=imgurl, startingbid=bid, category=category_instance )
        newlisting.save()
        return HttpResponseRedirect(reverse("index"))
    
def listing_detail(request,listing_id):
    listing=Auction_listings.objects.get(id=listing_id)
    comments=Comments.objects.filter(listing=listing_id)
    if request.user.is_authenticated:
        T_F = Watchlist.objects.filter(user=request.user, listing=listing).exists()
    else:
        T_F = False
    if request.method=="GET":
        return render(request, "auctions/listing_detail.html",{
        "listing":listing,
        "T_F":T_F,
        "comments":comments,
        })
    else:
        user=request.user
        listing_instance=Auction_listings.objects.get(id=listing_id)
        watchlist_item=Watchlist(user=user,listing=listing_instance)
        watchlist_item.save()
        return HttpResponseRedirect(reverse("index"))



def categories(request):
    categories=Category.objects.all()
    return render(request, "auctions/category.html",{
        "categories": categories,
    })

def category_name(request,category_name):
    category = get_object_or_404(Category, name=category_name)
    listing=Auction_listings.objects.filter(category=category, is_active=True)
    heading=f'Active listings of {category.name} cars'
    return render(request, "auctions/index.html",{
        "listings":listing,
        "heading":heading
    })
    
def remove(request,listing_id):
    listing=Auction_listings.objects.get(id=listing_id)
    watchlist_item = Watchlist.objects.filter(user=request.user, listing=listing)
    watchlist_item.delete()
    return HttpResponseRedirect(reverse("listing_detail", args=[listing_id]))

def add(request,listing_id):
    listing=Auction_listings.objects.get(id=listing_id)
    Watchlist.objects.create(user=request.user, listing=listing)
    return HttpResponseRedirect(reverse("listing_detail", args=[listing_id]))

def watchlist(request):
    user=request.user
    watchlist_items=Watchlist.objects.filter(user=user)
    listings=[item.listing for item in watchlist_items]
    return render(request,'auctions/index.html',{
        "listings":listings,
        "heading":"Watchlist"
    })

def add_comments(request,listing_id):
    user=request.user
    listing=Auction_listings.objects.get(id=listing_id)
    content=request.POST['content']
    newcomment=Comments(user=user,listing=listing,content=content)
    newcomment.save()
    return HttpResponseRedirect(reverse("listing_detail",args=[listing_id]))

def add_bid(request,listing_id):
    user=request.user
    listing=Auction_listings.objects.get(id=listing_id)
    if user==listing.Owner:
        messages.warning(request, "You cannot bid on your own item.")
        return HttpResponseRedirect(reverse("listing_detail", args=[listing_id]))
    
    bid=request.POST['bid']
    bid__=Decimal(bid)
    newbid=Bids(user=user,bid=bid__)
    newbid.save()
    listing.startingbid=newbid
    listing.save()
    messages.success(request, "Your bid has been placed successfully!")

    return HttpResponseRedirect(reverse("listing_detail", args=[listing_id]))

def close(request,listing_id):
    listing=Auction_listings.objects.get(id=listing_id)
    listing.is_active=False
    listing.save()
    highest_bid = listing.startingbid
    messages.success(request, "Auction closed successfully!")

    return HttpResponseRedirect(reverse("listing_detail", args=[listing_id]))
    
