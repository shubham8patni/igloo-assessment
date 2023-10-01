from django.db import models

# Create your models here.
class Products(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=80, unique=True, null=False)
    product_description = models.TextField(max_length=350)
    product_price = models.IntegerField(null=False)


