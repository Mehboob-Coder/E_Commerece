import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from Account.helpers import send_email_to_user
from .models import *
from E_Commerece import settings
from django.contrib.auth.decorators import login_required
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
@login_required
def checkout_cart(request ):
    if request.method == "POST":
        product_id = request.POST.get("prod_id")
        print(product_id)
        products = get_object_or_404(ProductModel, id=product_id)
        AddToCart.objects.get_or_create(
            user=request.user,product=products, image=products.image, price=products.price, 
            defaults={'price':products.price,'image':products.image ,'quantity':1}
        )
        return redirect('/checkout_cart/')
        
    amount = 0
    shipping = 0 
    total_amount = 0
    cart_items = AddToCart.objects.filter(user=request.user)

    if cart_items:
        for cart in cart_items:
            cart.total_price = cart.price * cart.quantity
            total_price  = cart.price * cart.quantity
            shipping +=cart.quantity * 8
            amount += total_price
            total_amount += shipping + total_price
    context={"cart_items": cart_items, 
             "amount":amount,
             "shipping":shipping,
             "subtotal":total_amount,
              }
    return render(
        request,"checkout_cart.html",context=context,)

def increment_quan(request,id):
    user =request.user
    print(id)
    cart_item  = get_object_or_404(AddToCart,id=id, user=user)
    cart_item.quantity +=1
    cart_item.save()
    return redirect('checkout_cart')

def decrement_quan(request,id):
    user = request.user
    cart_item  = get_object_or_404(AddToCart,id=id ,user=user)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    return redirect('checkout_cart')

def DeleteProduct(request,id):
    user = request.user
    product_id = get_object_or_404(AddToCart,id=id,user=user)
    product_id.delete()
    return redirect('checkout_cart')


@login_required  
def checkout_complete(request):
    items = AddToCart.objects.filter(user=request.user).first()
    cart_items = AddToCart.objects.filter(user=request.user)
    total_amount = 0
    for i in cart_items:
        price=i.price
        quantity = i.quantity
        total_amount += price * quantity
        image=i.image
        name = i.product.item_title

        odr_prd_mod = OrderProductDetails.objects.create(user=request.user,name=name,image=image,price=price,quantity=quantity)
        odr_prd_mod.save()
        
        
        print(f"Total amount calculated: {total_amount}")
   
    date = datetime.datetime.now()
    delivery_date_delta = datetime.timedelta(days=2)
    delivery_date = date + delivery_date_delta
    
    transaction = "REF" 
    bank_authorised_code = "AUTH" 

    cart_items_list = list(cart_items)

    cart_items.delete()

    context = {
        'total_amount': total_amount,
        'items': items,
        'cart_items': cart_items_list, 
        'date': date,
        'delivery_date': delivery_date,
        'transaction_reference_no': transaction,
        'bank_authorised_code': bank_authorised_code,
    }
    return render(request, "checkout_complete.html", context)
@login_required
def checkout_info(request):
       
    error = []
    context = {'error': error}
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company_name = request.POST.get('company_name')
        area_code = request.POST.get('area_code')
        primary_phone = request.POST.get('primary_phone')
        address_1 = request.POST.get('address_1')
        address_2 = request.POST.get('address_2')
        street_address = f"{address_1} {address_2}".strip()
        zip_code = request.POST.get('zip_code')
        business_address = request.POST.get('business_address')

        
        if not first_name:
            error.append("Invalid user name")
        if not last_name:
            error.append("Invalid last name")
        if not area_code or len(area_code)<3:
            error.append("Invalid area code")
        if not primary_phone:
            error.append("Invalid primary phone")
        if not street_address:
            error.append("Invalid street address")
        if not zip_code:
            error.append("Invalid zip code")

        if not error:
            shipping_address = ShippingAddress(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                area_code=area_code,
                primary_phone=primary_phone,
                street_address=street_address,
                zip_code=zip_code,
                business_address=business_address
            )
            shipping_address.save()
            return redirect('checkout_payment')
    return render(request, "checkout_info.html",context)
@login_required
def checkout_payment(request):
    user_cart_items = AddToCart.objects.filter(user=request.user)
    if user_cart_items.exists():
        line_items = []
        for cart_item in user_cart_items:
            product = cart_item.product
            name = product.item_title
            price = product.price
            line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(price * 100),
                        'product_data': {'name': name},
                    },
                    'quantity': cart_item.quantity,
                })
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('checkout_complete')),
            cancel_url=request.build_absolute_uri(reverse('home')),
            line_items=line_items,
            )
        send_email_to_user()
        return redirect(session.url)
    return render(request, "checkout_payment.html")
@login_required
def contact_us(request):

    try:
        if request.method == 'POST':
            name = request.POST.get("name")
            email = request.POST.get("email")
            subject = request.POST.get("subject")
            message = request.POST.get("message")

            ContactModel =ContactUs.objects.create(name=name,email=email,subject=subject,message=message)
            ContactModel.save()


            return redirect("contact_us")
        
        else:
            return render(request, "contact_us.html")

    except Exception as e:
        print(f"Something went wrong${e}")

def faq(request):
    faq = Faq.objects.all()
    
    data = {
        'faq':faq,
    }
    return render(request, "faq.html",data )
@login_required
def my_account(request):
    return render(request, 'my_account.html')
@login_required
def search_results(request):
    return render(request, 'search_results.html')
@login_required
def about_us(request):

    abt_us_mod = AboutUs.objects.all()
    data ={'abt_us_mod':abt_us_mod}

    return render(request, 'about_us.html', data)
@login_required
def header(request):
    cart_items = AddToCart.objects.all()
    
    data={
        "cart_items":cart_items,
    }
    return render(request,'header.html',data)

