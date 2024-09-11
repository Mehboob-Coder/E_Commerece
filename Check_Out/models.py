from django.db import models
from django.contrib.auth.models import User
from Product.models import *

# Create your models here.
class AddToCart(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True)
    price=models.IntegerField(default=0)
    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self) -> str:
        return self.product.brand.brand_name
    
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name =models.CharField(max_length=100)
    last_name =models.CharField(max_length=100)
    company_name =models.CharField(max_length=100, blank=True, null=True)
    area_code =models.CharField(max_length=100)
    primary_phone = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    business_address = models.BooleanField(default=False,blank=True,null=True)


    def __str__(self):
        return self.user.username

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email =models.EmailField(default="123@gmail.com")
    subject = models.CharField(max_length=100)
    message =models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name

class OrderProductDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(null=True ,blank=True)
    price = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=100)

class Faq(models.Model):
    question =  models.CharField(max_length=100)
    answer = models.CharField(max_length=500)
class AboutUs(models.Model):
    heading = models.CharField(max_length=100)
    paragraph =models.CharField(max_length=100) 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='main_profile')
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username