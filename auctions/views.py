from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Max
from .models import User, Catagory, Listing, bids, comments
from django import forms
    
    
class NewTaskForm(forms.Form):
    task = forms.CharField(max_length=20,label="New Task")


def index(request):
    if request.method == 'GET':
        activeListings = Listing.objects.filter(isActive=True)
        allCategories = Catagory.objects.all()

        return render(request, "auctions/index.html", {
            'listings': activeListings, 'categories': allCategories
        })


def Listingself(request, pk):
    if request.method == 'GET':
        user = request.user
        listingData = Listing.objects.get(pk=pk)
        isListingInWatchList = request.user in listingData.watchlist.all()
        bdiss = bids.objects.filter(ListID=pk)
        
        try:
            max_amount = bdiss.aggregate(bidsa=Max('bidsa'))['bidsa']
            bdiss = bids.objects.filter(bidsa=max_amount)
            
        except ObjectDoesNotExist:
            max_amount = None  # Set max_amount to None or any other appropriate value
            bdiss = None  # Set bdiss to None or any other appropriate value
        except TypeError:
            max_amount = None
            bdiss = None
        
        all_listings = Listing.objects.filter(pk=pk)
        commentt = list(comments.objects.filter(list_ID=pk))
        reversed_comment = list(reversed(commentt))
        bidusername = bids.objects.filter(pk=pk)
        return render(request, 'auctions/Listing.html', {'isListingInWatchList': isListingInWatchList,
                                                        'commentt': reversed_comment,
                                                        'all_listings': all_listings,
                                                        'bdiss': bdiss,
                                                        'max_amount': max_amount,
                                                        'bidusername': bidusername,
                                                        'user': user,})


def closeAction(request, pk):
    listingData = Listing.objects.get(pk=pk)
    listingData.isActive = False
    listingData.save()
    winerName = request.POST.get('winner.name')
    number = request.POST.get('winner.id')
    
    message = f"congrats {winerName} {number}"
    return  redirect(reverse('Listingself', args=(pk,)))


def bid(request, pk):
    if request.method == 'POST':
        userbid = request.POST.get('bid')
        currentuser = request.user
        listIdd = request.POST.get('listing_id')
        calistname1 = Listing.objects.get(pk=pk)
        existing_bid = bids.objects.filter(
            bidsa=userbid, owner=currentuser, listname=listIdd, ListID=listIdd)
        message = ''
        if existing_bid.exists():
            message = 'Bid Already exists'
            return redirect(reverse('Listingself', args=(pk,)))
        else:
            new_bid = bids(bidsa=userbid, owner=currentuser,
                           listname=calistname1, ListID=listIdd)
            new_bid.save()
            return redirect(reverse('Listingself', args=(pk,)))


def commentsa(request, pk):
    if request.method == 'POST':
        req_user_ID = request.user
        req_list_id = request.POST.get('listing_id')
        req_comment = request.POST.get('comenta')
        List_id = Listing.objects.get(pk=req_list_id)
        new_comment = comments(
            list_ID=List_id,
            user_ID=req_user_ID,
            comment=req_comment,
        )
        new_comment.save()
        return redirect(reverse("Listingself", args=(pk,)))


def delete_comment(request, pk):
    if request.method == 'POST':
        user = request.user
        dd = request.POST.get('comment-pk')
        commentid = request.POST.get('comment-id')
        skrt = request.POST.get('coment')
        comment = comments.objects.get(comment=skrt)
        comment.delete()
        return redirect(reverse("Listingself", args=(pk,)))


@login_required
@csrf_protect
def watchlist(request):
    current_user = request.user
    watchedlists = Listing.objects.filter(watchlist = current_user)
    return render(request, "auctions/watchlist.html", {'watchedlists': watchedlists})


def addWathcList(request, pk):
    ListingData = Listing.objects.get(pk=pk)
    current_user = request.user
    ListingData.watchlist.add(current_user)
    ListingData.save()
    return redirect(reverse("index"))


def removewatchList(request, pk):
    ListingData = Listing.objects.get(pk=pk)
    current_user = request.user
    ListingData.watchlist.remove(current_user)
    ListingData.save()
    return redirect(reverse("Listingself", args=(pk,)))


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
            else:
                newcategeo = Catagory(categoryName=newCategory)
                newcategeo.save()
            return HttpResponseRedirect(reverse("index"))
        


def TT(request):
    return render(request, "auctions/selectedCategory.html")


def displayCategory(request):
    if request.method == 'POST':
        selectedCategory = request.POST.get('category')
        category = Catagory.objects.get(categoryName=selectedCategory)
        activeListings = Listing.objects.filter(
            isActive=True, category=category)
        allCategories = Catagory.objects.all()
        return render(request, "auctions/index.html", {
            'listings': activeListings, 'categories': allCategories
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