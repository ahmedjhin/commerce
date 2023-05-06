from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Catagory, Listing
from .form import MyForm

def index(request):
    if request.method == 'GET':
        activeListings = Listing.objects.filter(isActive=True)
        allCategories = Catagory.objects.all()
        return render(request, "auctions/index.html",{
        'listings': activeListings,'catagories':allCategories
        })
    

def creatCategory(request):
    if request.method == 'GET':
        creatCategory = Catagory.objects.all()
        return render(request, "auctions/creatCategory.html",{'creatCategory':creatCategory})
    else:
        newCategory = request.POST.get('cateonew')

        newcategeo = Catagory(
           categoryName = newCategory
        )

        newcategeo.save()
        return HttpResponseRedirect(reverse(index))

def displayCategory(request):
    if request.method == 'POST':
        selectedCategory = request.POST.get('category')
        category = Catagory.objects.get(categoryName=selectedCategory)
        activeListings = Listing.objects.filter(isActive=True,category=category)
        allCategories = Catagory.objects.all()
        return render(request, "auctions/index.html",{
        'listings': activeListings,'catagories':allCategories
        })

def createListeing(request):
    if request.method == 'GET':
        allCategories = Catagory.objects.all()
        return render(request, "auctions/create.html",{'catagories':allCategories})
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