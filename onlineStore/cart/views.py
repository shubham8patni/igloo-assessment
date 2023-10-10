from django.shortcuts import render
from rest_framework.response  import Response
from .serializers import cartSerializer, GetcartSerializer
from rest_framework.views import APIView
from .models import Cart
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
import json
import redis
from .helper import primary_cache
# Create your views here.

r = redis.Redis(host='127.0.0.1', port=6379, db=0)  #redis://127.0.0.1:6379

class cart(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]


    def get(self, request, *args, **kwargs):
        user = request.user

        # r.delete(f"{user}")
        #### CACHE ####
        cached_data = r.hgetall(f"{user}")
        if cached_data is {}:
            resp = primary_cache(r, user)
            
        elif not cached_data:
            resp = primary_cache(r, user)
            
        else:
            resp = list(cached_data.values())
            resp = [json.loads(json_string) for json_string in resp]
            payload = {
                'products':  resp,
                'total_items' : sum(item["quantity_of_product"] for item in resp),
                'total_cart_price' :  sum(item['quantity_of_product']*item['product_price'] for item in resp),
            }
            return Response({
                'statusCode' : 200,
                'body' : payload
            })
            
        return Response({
            'statusCode' : 200,
            'body' : resp
        })
    
    @method_decorator(ratelimit(key='user', rate='1/3s', method='POST', block=True))
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
            
            #### CACHE ####
            cached_data = r.hgetall(f"{payload['user_id']}")
            if cached_data is {}:
                primary_cache(r, user)
            elif not cached_data:
                primary_cache(r, user)
            else:
                pass

            serialized_data = GetcartSerializer(existing_prod)
            cached_prod = r.hmget(f"{payload['user_id']}", f"product {payload['product_id']}")
            if cached_prod[0] is None:
                r.hmset(f"{payload['user_id']}", {f"product {payload['product_id']}" : json.dumps(serialized_data.data)})
            else:
                cached_prod = json.loads(cached_prod[0].decode('utf-8'))
                cached_prod["quantity_of_product"] = serialized_data.data['quantity_of_product']
                r.hset(f"{payload['user_id']}", f"product {payload['product_id']}", json.dumps(cached_prod))
            r.expire(f"{payload['user_id']}", 300)

            return Response({
                    'status': 200,
                    'body' : f'Quantity Updated to {existing_prod.quantity_of_product}'
                })
        else:
            serialized_data =  cartSerializer(data= payload)
            if serialized_data.is_valid():
                serialized_data.save()

                #### CACHE ####
                cached_data = r.hgetall(f"{user}")
                if cached_data is {}:
                    primary_cache(r, user)
                elif not cached_data:
                    primary_cache(r, user)
                else:
                    pass

                cached_prod = r.hmget(f"{payload['user_id']}", f"product {payload['product_id']}")
                if cached_prod is None:
                    r.hmset(f"{payload['user_id']}", {f"product {payload['product_id']}" : json.dumps(serialized_data.data)})
                else:
                    cached_prod = json.loads(cached_prod[0].decode('utf-8'))
                    cached_prod["quantity_of_product"] = serialized_data.data['quantity_of_product']
                    r.hset(f"{payload['user_id']}", f"product {payload['product_id']}", json.dumps(cached_prod))
                r.expire(f"{payload['user_id']}", 300)

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
        
    @method_decorator(ratelimit(key='user', rate='1/3s', method='DELETE', block=True))  # rate can be idealy set after/based on performance/load testing 
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

                #### CACHE ####
                cached_data = r.hgetall(f"{user}")
                if cached_data is {}:
                    primary_cache(r, user)
                elif not cached_data:
                    primary_cache(r, user)
                else:
                    pass

                serialized_data = GetcartSerializer(existing_prod)
                cached_prod = r.hmget(f"{user}", f"product {request.data['product_id']}")
                if cached_prod[0] is None:
                    r.hmset(f"{user}", {f"product {request.data['product_id']}" : json.dumps(serialized_data.data)})
                else:
                    cached_prod = json.loads(cached_prod[0].decode('utf-8'))
                    cached_prod["quantity_of_product"] = serialized_data.data['quantity_of_product']
                    r.hset(f"{user}", f"product {request.data['product_id']}", json.dumps(cached_prod))
                r.expire(f"{user}", 300)

            elif existing_prod.quantity_of_product == 1:
                existing_prod.delete()
                #### CACHE ####
                r.delete(f"{user}")
            return Response({
                        'status': 204,
                    })
        except Exception as e:
            return Response({
                        'status': 404,
                        'body' : 'Product not in cart'
                    })
 