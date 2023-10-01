from django.urls import path
from .views import cart

urlpatterns = [
    # path('<int:id>', cart.as_view(), name='user_cart'),
    path('', cart.as_view(), name='user_cart'),
    
]
