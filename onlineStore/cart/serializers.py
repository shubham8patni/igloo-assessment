from rest_framework import serializers
from .models import Cart
from app1.models import Products

class cartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user_id', 'product_id', 'quantity_of_product']


class CartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['quantity_of_product']



class ProdSerialize(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['product_id', 'product_name', 'product_price']

class GetcartSerializer(serializers.ModelSerializer):
    product = ProdSerialize(source='product_id')
    class Meta:
        model = Cart
        fields = ['product', 'quantity_of_product']
