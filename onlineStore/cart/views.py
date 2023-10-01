from django.shortcuts import render
from rest_framework.response  import Response
from .serializers import cartSerializer, GetcartSerializer
from rest_framework.views import APIView
from .models import Cart
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

class cart(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def get(self, request, *args, **kwargs):
        user = request.user
        query = Cart.objects.filter(user_id = user)
        serialized_data = GetcartSerializer(query, many=True)

        payload = {
            'products':  serialized_data.data,
            'total_items' : sum(item["quantity_of_product"] for item in serialized_data.data),
            'total_cart_price' :  sum(item['quantity_of_product']*item['product']['product_price'] for item in serialized_data.data),
        }


        return Response({
            'statusCode' : 200,
            'body' : payload
        })
    

    def post(self, request, *args, **kwargs):
        user = request.user
        quantity_of_product = int(request.data.get('quantity_of_product', 1))

        if not request.data['product_id']:
            return Response({
                'status': 400,
                'body': 'Product ID is required'
            })
        
        payload = {
            'user_id' : request.user,
            'product_id' : request.data['product_id'],
            'quantity_of_product' : int(quantity_of_product)
        }
        if Cart.objects.filter(user_id = user, product_id = request.data['product_id']).exists():
            existing_prod = Cart.objects.get(user_id = user, product_id = request.data['product_id'])
            existing_prod.quantity_of_product += quantity_of_product
            existing_prod.save()
            return Response({
                    'status': 200,
                    'body' : f'Quantity Updated to {existing_prod.quantity_of_product}'
                })
        else:
            serialized_data =  cartSerializer(data= payload)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({
                    'status': 200,
                    'body' : 'Success'
                })
            else:
                return Response({
                    'status': 400,
                    'body' : serialized_data.errors
                })

    
    # def put(self, request):
        

    def delete(self, request, *args, **kwargs):
        user = request.user
        
        if not request.data['product_id']:
            return Response({
                'status': 400,
                'body': 'Product ID is required'
            })
        
        try :
            existing_prod = Cart.objects.get(user_id = user, product_id = request.data['product_id'])
            
            if existing_prod.quantity_of_product > 1:
                existing_prod.quantity_of_product -= 1
                existing_prod.save()
            elif existing_prod.quantity_of_product == 1:
                existing_prod.delete()

            return Response({
                        'status': 204,
                    })
        except Exception as e:
            return Response({
                        'status': 404,
                        'body' : 'Product not in cart'
                    })