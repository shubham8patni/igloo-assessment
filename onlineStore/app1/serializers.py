from rest_framework import serializers
from .models import Products

class productsserializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields =  '__all__' #['product_name', 'product_description', 'product_price']



