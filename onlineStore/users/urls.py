from django.urls import path
from .views import login, register
urlpatterns = [
    path('register/', register.as_view(), name='register'),
    path('login/', login.as_view(), name='login'),
]
