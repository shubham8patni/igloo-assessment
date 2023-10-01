from django.urls import path
from .views import products, product_details #, addtoDB

urlpatterns = [
    path('', products.as_view(), name='prod_list'),
    path('<int:id>', product_details.as_view(), name='prod_detail'),
    
]
