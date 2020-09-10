from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"
class Product(models.Model):
    title = models.CharField(max_length=255)
    startingBid = models.FloatField(default=0)
    Bid = models.FloatField()
    ImageUrl = models.CharField(max_length=500)
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="category")
    createdTime = models.DateField()
    seller = models.ForeignKey(User,on_delete=models.CASCADE,related_name="seller")
    active = models.BooleanField(default=1)
    owner = models.IntegerField()
    
    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    buyer = models.ForeignKey(User,on_delete=models.CASCADE,related_name="buyer")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product")
    bid = models.FloatField()

    def __str__(self):
        return f"{self.bid}$ to {self.product} from {self.buyer}"

class Comment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="author")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="productid")
    commentTitle = models.CharField(max_length=64)
    comment = models.TextField()

    def __str__(self):
        return f"{self.author}"

class Wishlist(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="wisher")
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="wishproductid")

    def getUser(self):
        return self.user_id
    def getProduct(self):
        return self.product_id