from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
# Create your models here.
class Category(models.Model):
    DEVISE_CHOICES =[
        ("Mobile","Mobile"),
        ("Tablet","Tablet"),
        ("Laptop","Laptop"),
        ("Watch","Watch"),
        ("Gadget","Gadget"),
        ("Speaker","Speaker"),
        ("Accessories","Accessories"),
        ("Computer","Computer"),
        ("TV","TV"),
    ]
    name =models.CharField(max_length=100, choices=DEVISE_CHOICES)
    def __str__(self) -> str:
        return self.name

class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    category =models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.brand_name
class ProductModel(models.Model):
    category =models.ForeignKey(Category, on_delete=models.CASCADE)
    brand =models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="assets/img/")
    item_title = models.CharField(max_length=100)
    item_desc = models.TextField(max_length=100)
    off= models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    item_discount_price=models.IntegerField(default=0)
    Trending_product = models.BooleanField(default=False,help_text="@-default,1-Trending")

    # def __str__(self) -> str:
    #     return self.item_title

class Promotions(models.Model):
    product =models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    first = models.BooleanField(default=False)
    seconds = models.BooleanField(default=False)
    third = models.BooleanField(default=False)
    forth = models.BooleanField(default=False)
    fifth = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.product.item_title

class Slider(models.Model):
    product =models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    back = models.ImageField(upload_to="assets/img/")
    first = models.BooleanField(default=False)
    seconds = models.BooleanField(default=False)
    third = models.BooleanField(default=False)

    # def __str__(self) -> str:
    #     return self.product.item_title
class ProductDescription(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to="assets/img/")



class Review(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    review = models.CharField(max_length=150)
    rating = models.IntegerField(default=0)

    def clean(self):
        if not (1 <= self.rating <= 5):
            raise ValidationError("Rating must be between 1 and 5")
