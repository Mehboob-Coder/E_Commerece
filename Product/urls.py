from django.urls import path
from . views import *
urlpatterns=[
    
    path('home',home, name='home'),
    
    path('index_fixed_header',index_fixed_header, name ='index_fixed_header'),
    path('index_inverse_header',index_inverse_header, name ='index_inverse_header'),
    # path("product_view/<slug:pk>",product_list_view,name="product_view"),
    path('product_detail/<int:id>',product_detail, name ='product_detail'),
    path('product',product, name ='product'),
    
]