from django.urls import path
from . views import *

urlpatterns = [
    
    path('checkout_cart/',checkout_cart, name ='checkout_cart'),
    path('checkout_complete',checkout_complete, name ='checkout_complete'),
    path('checkout_info',checkout_info, name ='checkout_info'),
    path('checkout_payment',checkout_payment, name ='checkout_payment'),
    path('contact_us',contact_us, name ='contact_us'),
    path('faq',faq, name ='faq'),
    path('my_account',my_account, name ='my_account'),
    path('search_results',search_results, name ='search_results'),
    path('about_us',about_us, name ='about_us'),
    path("increment_quan/<int:id>/", increment_quan, name="increment_quan"),
    path("decrement/<int:id>/", decrement_quan, name="decrement_quan"),
    path('delete/<int:id>',DeleteProduct,name='DeleteProduct'),
]