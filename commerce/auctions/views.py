from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User,Category,Product,Comment,Bid,Wishlist

from datetime import datetime




class NewProduct(forms.Form):
    pass

def index(request):
    products = Product.objects.filter(active=1)
    return render(request, "auctions/index.html",{
            "products" : products
    })

def listings(request,listing_id):
    product = Product.objects.get(pk=listing_id)
    comments = Comment.objects.filter(product=listing_id)
    bids = Bid.objects.filter(product=listing_id)
    try:
        owner = User.objects.get(pk=product.owner)
    except:
        owner = ""

    user = request.user

    try :
        wishlist = Wishlist.objects.get(user_id=user,product_id=product)
        if wishlist.user_id.id == user.id:
            return render(request, "auctions/listings.html", {
            "product" : product,
            "comments" : comments,
            "bids" : bids,
            "owner" : owner,
            "addedwish" : wishlist
        })

    except:
        return render(request,"auctions/listings.html",{
            "product" : product,
            "comments" : comments,
            "bids" : bids,
            "owner" : owner
        })

def comment(request,listing_id):
    if request.method == "POST":
        title = request.POST["title"]
        comment = request.POST["comment"]
        
        product = Product.objects.get(pk=listing_id)

        user = User.objects.get(pk=request.user.id)

        addComment = Comment(product=product,author=user,commentTitle=title,comment=comment)
        addComment.save()

        return HttpResponseRedirect(reverse("listing",args=(listing_id,)))

def bid(request,listing_id):
    if request.method == "POST":
        bid = float(request.POST["bid"])
        
        product = Product.objects.get(pk=listing_id)
        user = User.objects.get(pk=request.user.id)
        

        comments = Comment.objects.filter(product=listing_id)
        
        bids = Bid.objects.filter(product=listing_id)
        if product.owner != 0:
            owner = User.objects.get(pk=product.owner)

        owner = ""

        if bid <= float(product.Bid) or bid <= float(product.startingBid) :
            comments = Comment.objects.filter(product =listing_id)
            return render(request,"auctions/listings.html",{
                "product" : product,
                "comments" : comments,
                "bids" : bids,
                "warningmessage" :  "You can't offer a bid lower than the product's current price.",
                "owner" : owner

            })  

        elif user.id == product.seller.id:
            return render(request,"auctions/listings.html",{
                "product" : product,
                "comments" : comments,
                "bids" : bids,
                "warningmessage" :  "You can't offer a bid your product.",
                "owner" : owner
            }) 

        if user.id == product.owner :
            return render(request,"auctions/listings.html",{
                "product" : product,
                "comments" : comments,
                "bids" : bids,
                "warningmessage" :  "You can't offer a bid again.",
                "owner" : owner
            }) 

        else:
            addBid = Bid(buyer=user,product=product,bid=bid)
            addBid.save()
            product.Bid = bid
            product.save()
            product.owner = user.id
            product.save()
            owner = User.objects.get(pk=product.owner)
            return render(request,"auctions/listings.html",{
                "product" : product,
                "comments" : comments,
                "bids" : bids,
                "successmessage" :  "Succesfull !",
                "owner" : owner
            })    

def createlisting(request):
    if request.method == "POST":
        title = request.POST["title"]
        startingBid = request.POST["startingbid"]
        Bid = 0
        ImageUrl = request.POST["imageurl"]
        description = request.POST["description"]
        category = Category.objects.get(pk=int(request.POST["category"]))
        createdTime = datetime.now()
        seller = request.user
        owner = 0
        addProduct = Product(title=title,startingBid=startingBid,Bid=Bid,ImageUrl=ImageUrl,description=description,category=category,createdTime=createdTime,seller=seller,owner=owner)
        addProduct.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        categories = Category.objects.all()
        return render(request,"auctions/createlisting.html",{
            "categories": categories
        })

def categories(request):
    categories = Category.objects.all()
    return render(request,"auctions/categories.html",{
        "categories":categories
    })


def wishlistget(request):
    user = request.user

    wishlist = Wishlist.objects.filter(user_id=user)

    return render(request, "auctions/wishlist.html", {
        "wishlist":wishlist
    })

def wishlist(request,listing_id):
    if request.method == "POST":
        user = request.user

        product = Product.objects.get(pk=listing_id)  

        comments = Comment.objects.filter(product=listing_id)
        
        bids = Bid.objects.filter(product=listing_id)

        owner = User.objects.get(pk=product.owner)
        
        
        try :
            wishlist = Wishlist.objects.get(user_id=user,product_id=product)

            if wishlist.user_id.id == user.id:
                return render(request, "auctions/listings.html", {
                "warningwish": "This product already added your wishlist.",
                "product" : product,
                "comments" : comments,
                "bids" : bids,
                "owner" : owner
            })

        except:
            addWish = Wishlist(user_id=user,product_id=product)          
            addWish.save()  
            return render(request, "auctions/listings.html", {
                    "successwish": "This product successfully added your wishlist.",
                    "product" : product,
                    "comments" : comments,
                    "bids" : bids,
                    "owner" : owner,
                    "addedwish" : 1
            })
            


def removewishlist(request,listing_id):
    user = request.user
    product = Product.objects.get(pk=listing_id)
    wishlist = Wishlist.objects.get(user_id=user,product_id=product)
    wishlist.delete()
    comments = Comment.objects.filter(product=listing_id)
        
    bids = Bid.objects.filter(product=listing_id)

    owner = User.objects.get(pk=product.owner)

    return render(request, "auctions/listings.html", {
        "successwish": "This product successfully removed your wishlist.",
        "product" : product,
        "comments" : comments,
        "bids" : bids,
        "owner" : owner,
        
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
