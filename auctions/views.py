from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from .models import User, Catagory, Listing, user_watchList, bids
from .form import MyForm


def index(request):
    if request.method == 'GET':
        activeListings = Listing.objects.filter(isActive=True)
        allCategories = Catagory.objects.all()
        return render(request, "auctions/index.html", {
            'listings': activeListings, 'categories': allCategories
        })


def Listingself(request, pk):
    if request.method == 'POST':
        userbid = request.POST.get('bid')
        currentuser = request.user
        listnameE = request.POST.get('listname')
        listIdd = request.POST.get('listing_id')
        calistname = Listing.objects.filter(pk=pk)
        calistname1 = Listing.objects.get(pk=pk)
        existing_bid = bids.objects.filter(bidsa=userbid, owner=currentuser, listname=listIdd, ListID=listIdd)
        message = ''
        if existing_bid.exists():
            all_listings = Listing.objects.filter(pk=pk)
            message = 'You have already placed a bid with the same price.'
            return render(request, 'auctions/Listing.html', {'all_listings': all_listings, 'message': message})
        else:
            bidforthis_list = bids.objects.filter(ListID=listIdd)
            new_bid = bids(bidsa=userbid, owner=currentuser,
                           listname=calistname1, ListID=listIdd)
            new_bid.save()
            all_listings = Listing.objects.filter(pk=pk)
            return render(request, 'auctions/Listing.html', {'all_listings': all_listings, 'bidforthis_list': bidforthis_list})
    else:
        if request.method == 'GET':
            listingstitle = request.GET.get('listing_id')
            bidforthis_list = bids.objects.filter(ListID=listingstitle)
            all_listings = Listing.objects.filter(pk=pk)
            currentuser = request.user
            listnamer = request.GET.get('listing_title')
            listnameE = Listing.objects.get(title=listnamer)
            listIdd = request.GET.get('listing_id')

            all_listings = Listing.objects.filter(pk=pk)

            all_listings = Listing.objects.filter(pk=pk)
            return render(request, 'auctions/Listing.html', {'all_listings': all_listings, 'bidforthis_list': bidforthis_list})


@login_required
@csrf_protect
def watchlist(request):
    if request.method == 'POST':
        listing_id = request.POST.get('listing_id')
        username = request.user
        watchedListing = Listing.objects.filter(id=listing_id,)
        newWatchList = user_watchList(
            ownerWatchList=username, idNumber=listing_id)
        existing_watchlist = user_watchList.objects.filter(
            ownerWatchList=username, idNumber=listing_id)
        if existing_watchlist.exists():

            return render(request, "auctions/Watchlist.html", {'watchedListing': watchedListing})
        else:
            newWatchList.save()
            return render(request, "auctions/watchlist.html", {'watchedListing': watchedListing})
    else:
        if request.method == 'GET':
            current_user = request.user
            user_watchlists = user_watchList.objects.filter(
                ownerWatchList=current_user)
            watched_listing_ids = [
                watchlist.idNumber for watchlist in user_watchlists]
            all_listings = Listing.objects.filter(id__in=watched_listing_ids)
        return render(request, "auctions/watchlist.html", {'all_listings': all_listings, })


def creatCategory(request):
    if request.method == 'GET':
        creatCategory = Catagory.objects.all()
        return render(request, "auctions/creatCategory.html", {'creatCategory': creatCategory})
    else:
        if request.method == 'POST':
            newCategory = request.POST.get('cateonew')
            if newCategory == "":
                message = "Couldn't find category"
                return render(request, "auctions/creatCategory.html", {'message': message})

        newcategeo = Catagory(
            categoryName=newCategory
        )

        newcategeo.save()
        return HttpResponseRedirect(reverse(index))


def displayCategory(request):
    if request.method == 'POST':
        selectedCategory = request.POST.get('category')
        category = Catagory.objects.get(categoryName=selectedCategory)
        activeListings = Listing.objects.filter(
            isActive=True, category=category)
        allCategories = Catagory.objects.all()
        return render(request, "auctions/index.html", {
            'listings': activeListings, 'catagories': allCategories
        })


def createListeing(request):
    if request.method == 'GET':
        allCategories = Catagory.objects.all()
        return render(request, "auctions/create.html", {'catagories': allCategories})
    else:
        title = request.POST.get('title')
        description = request.POST.get('Description')
        imageUrl = request.POST.get('ImageUrl')
        price = request.POST.get('Price')
        category = request.POST.get('category')

        currentUser = request.user

        categoryData = Catagory.objects.get(categoryName=category)

        newListing = Listing(
            title=title,
            description=description,
            imageUrl=imageUrl,
            price=float(price),
            category=categoryData,
            owner=currentUser
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))


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
