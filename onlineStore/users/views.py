from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response 
from django.contrib.auth import authenticate
# Create your views here.


class register(APIView):

    def post(self, request):
        try:
            serialized_data = UserSerializer(data=request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                user = User.objects.get(username=serialized_data.data['username'])
                refresh = RefreshToken.for_user(user=user)

                return Response({
                    'status' : 200,
                    'refresh_token' : str(refresh),
                    'access' : str(refresh.access_token),
                    'body' : 'Registration Successful'
                })
            else:
                return Response({
                    'status' : 400,
                    'body' : serialized_data.errors
                })
        except Exception as e:
            return Response({
                'status' : 400,
                'error' : str(e)
            })
        

class login(APIView):
    def post(self, request):
        try:
            serialized_data = LoginSerializer(data=request.data)
            if serialized_data.is_valid():
                username = serialized_data.data['username']
                password = serialized_data.data['password']
                user = authenticate(username=username,password=password)
                if user is None:
                    return Response({
                        'statusCode' : 400,
                        'body' : 'Invalid Credentials!'
                    })
                
                refresh = RefreshToken.for_user(user=user)
                return Response({
                    'status' : 200,
                    'refresh_token' : str(refresh),
                    'access' : str(refresh.access_token),
                })
            else:
                return Response({
                    'status' : 400,
                    'body' : serialized_data.errors
                })

        except Exception as e:
            return Response({
                'status' : 400,
                'error' : str(e)
            })


