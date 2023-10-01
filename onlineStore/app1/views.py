from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from .models import Products
from .serializers import productsserializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.


class products(APIView):
    permission_classes=  [IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def get(self, request, *args, **kwargs):
        query=Products.objects.all()
        serialized_data = productsserializer(query, many=True)
        return Response({
            'statusCode':200,
            'body':serialized_data.data
        })
    

class product_details(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def get(self, request, id, *args, **kwargs):
        try:
            query = Products.objects.get(product_id=id)
            
            serialized_data = productsserializer(query)
            return Response({
                'statusCode':200,
                'body':serialized_data.data
            })
        except Exception as e:
            return Response({
                'statusCode': 404,
                'body':  'Product not found!' #str(e)
            })

