from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def home(request):
    ##mobile
    mobile = request.POST.get('mobile',None)
    
    print(mobile)
    if mobile:
        mobile_products =ProductModel.objects.filter(category__name="Mobile",brand__brand_name=mobile)[:6]
    else:
        mobile_products=ProductModel.objects.filter(category__name="Mobile")
    mobile_products = mobile_products[:6]
    user = request.user
    
##trending
    trending_product  = ProductModel.objects.filter(Trending_product=1)[:6]
##tablet
    brand_name = Brand.objects.all()
    

    category = Category.objects.all()

    
    selected_brand = request.GET.get('tablet', None)
    
    if selected_brand:
       products = ProductModel.objects.filter  (brand__brand_name=selected_brand, category__name="Tablet")[:6]
    else:
        products = ProductModel.objects.filter  (category__name="Tablet")
        
    tablet_products = products[:6]

##Header
    product_apple=ProductModel.objects.filter(brand__brand_name="Apple")
    product_Samsung=ProductModel.objects.filter(brand__brand_name="	Samsung")
    product_sony=ProductModel.objects.filter(brand__brand_name="Sony")
    product_microsoft=ProductModel.objects.filter(brand__brand_name="Microsoft")

###pormotion
    first_promotion =Promotions.objects.filter(first=True).first()
    second_promotion =Promotions.objects.filter(seconds=True).first()
    third_promotion =Promotions.objects.filter(third=True).first()
    forth_promotion =Promotions.objects.filter(forth=True).first()
    fifth_promotion =Promotions.objects.filter(fifth=True).first()

###Sliders   
    first_slider =Slider.objects.filter(first=True).first()
    second_slider =Slider.objects.filter(seconds=True).first()
    third_slider=Slider.objects.filter(third=True).first()

   

    data = {

        'user':user, #user
        "mobile_products": mobile_products, #mobile
        "tablet_products": tablet_products,#tablet
        'Trending_product':trending_product,#trending
        'first_promotion':first_promotion, #promotion
        'second_promotion':second_promotion, #promotion
        'third_promotion':third_promotion, #promotion
        'forth_promotion':forth_promotion, #promotion
        'fifth_promotion':fifth_promotion, #promotion
        'first_slider':first_slider, #slider
        'second_slider':second_slider, #slider
        'third_slider':third_slider, #slider

        ##Header
        'product_apple':product_apple,
        'product_Samsung':product_Samsung,
        'product_sony':product_sony,
        'product_microsoft':product_microsoft,
        ##categorie
        "category":category,
    }

    return render(request, 'index.html', data)


def index_fixed_header(request):
    return render(request, 'index_fixed_header.html')
def index_inverse_header(request):
    return render(request, 'index_inverse_header.html')

@login_required(login_url='/login/')
def product_detail(request, id):
    # products = product_mod.objects.filter(category__id=pk, )
    # print(products)
    product = get_object_or_404(ProductModel, id=id)
    product_desc = ProductDescription.objects.all()
    reviews = Review.objects.filter(product=product)

    if request.method == "POST":
        name = request.POST.get("name")
        title = request.POST.get("Title")
        review = request.POST.get("review")
        rating = int(request.POST.get("rating"))
        print(review)
        try:
            product = ProductModel.objects.get(id=id)
        except ProductModel.DoesNotExist:
            
            print("Product does not exist.")
        else:
   
            review = Review(product=product, rating=5)
            review.save()

        try:
            new_review = Review(
                product=product, name=name, title=title, review=review, rating=rating
            )
            new_review.full_clean()
            new_review.save()
        except ValidationError as e:
            context = {
                "product": product,
                "product_desc": product_desc,
                "reviews": reviews,
            }

        return redirect("product_detail", id=id)

    context = {
        "product": product,
        "product_desc": product_desc,
        "reviews": reviews,
    }
    return render(request, "product_detail.html", context=context)


@login_required(login_url='/login/')
def product(request):
    mobile_products = ProductModel.objects.filter(category__name="Mobile")
    tablet_products = ProductModel.objects.filter(category__name="Tablet")
    items = ProductModel.objects.all()
    categories = Category.objects.all()
    
    paginator = Paginator(items, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'items': page_obj,
        'categories': categories,
        'prod': categories,
        'mobile_products':mobile_products,
        'tablet_products':tablet_products,
    }
    
    return render(request, "product.html",context=context)

# def product_list_view(request, pk):
#     products = ProductModel.objects.filter(category__id=pk)
#     paginator = Paginator(products, 3)  # Show 10 products per page

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'products': page_obj,
#     }
#     return render(request, 'product.html', context=context)