from django.db import models
from app1.models import Products
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, to_field='username', db_index=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, default=0)
    quantity_of_product = models.IntegerField()