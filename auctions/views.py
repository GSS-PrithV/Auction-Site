from audioop import maxpp
from dataclasses import field
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm

from .models import User,Category,Listing,Bids,Comment

class AuctionForm(ModelForm):
    class Meta:
        model = Listing 
        fields = ['title','description','StartingBid','category','Thumbnail']

class BidForm(ModelForm):
    class Meta:
        model = Bids
        fields = ['amount']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Listing.objects.all()
    })

def auction(request, id):
    if Listing.objects.get(id=id) is None:
        return HttpResponseRedirect("Auction Doesn't Exist")
    else:
        current = Listing.objects.get(id=id)
        return render(request, "auctions/auctionpage.html",{ 
            'auction': current,
            'bid': BidForm(),
            'commentform': CommentForm()
        })

def close(request, id):
    auction = Listing.objects.get(id=id)
    if request.user == auction.owner:
        auction.active = False
        auction.save()
    return HttpResponseRedirect(reverse('auction', kwargs={'id': id}))

def newlisting(request):
    form = AuctionForm(request.POST, request.FILES)
    if form.is_valid():
        new = form.save(commit=False)
        new.owner = request.user
        new.save()
        return HttpResponseRedirect(reverse('index')) 
    else:
        return render(request, "auctions/newlisting.html", {
            "form": form
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

def watch(request, id):
    if request.method == "POST":
        watchlist = request.user.watchlist
        if Listing.objects.get(id=id) in watchlist.all():
            watchlist.remove(Listing.objects.get(id=id))
        else:
            watchlist.add(Listing.objects.get(id=id))

    return HttpResponseRedirect(reverse('auction', kwargs={'id': id}))

def bidding(request, id):
    newbid = BidForm(request.POST)

    if newbid.is_valid():
        auction = Listing.objects.get(id=id)
        new = newbid.save(commit=False)

        if new.amount > auction.CurrentBid:
            new.auction = auction
            new.user = request.user
            new.save()
            auction.CurrentBid = new.amount
            auction.save()
            
    return HttpResponseRedirect(reverse('auction', kwargs={'id': id}))

def WatchList(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })

def category(request, catty):
    cat = Category.objects.get(category=catty)
    return render(request, "auctions/index.html", {
        "auctions": Listing.objects.filter(category=cat)
    })

def CategoryList(request):
    return render(request, "auctions/categorylist.html", {
        "categorylist" : Category.objects.all()
    })

def Comment(request, id):
    comment = CommentForm(request.POST)
    
    if comment.is_valid():
        new = comment.save(commit=False)
        new.auction = Listing.objects.get(id=id)
        new.user = request.user
        new.save()
    
    return HttpResponseRedirect(reverse('auction', kwargs={'id':id}))
    