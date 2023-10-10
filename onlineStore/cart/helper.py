from .serializers import cartSerializer, GetcartSerializer
from .models import Cart
import json

def primary_cache(r, user):

    query = Cart.objects.filter(user_id = user)
    serialized_data = GetcartSerializer(query, many=True)

    for item in serialized_data.data:
        r.hmset(f"{user}", {f"product {item['product_id']}" : json.dumps(item)})

    payload = {
            'products':  serialized_data.data,
            'total_items' : sum(item["quantity_of_product"] for item in serialized_data.data),
            'total_cart_price' :  sum(item['quantity_of_product']*item['product_price'] for item in serialized_data.data),
        }
    
    return payload







# [{"quantity_of_product":1,"product_id":2,"product_name":"Product 2","product_price":20},{"quantity_of_product":1,"product_id":3,"product_name":"Product 3","product_price":30},{"quantity_of_product":1,"product_id":4,"product_name":"Product 4","product_price":40},{"quantity_of_product":1,"product_id":7,"product_name":"Product 7","product_price":37},{"quantity_of_product":3,"product_id":9,"product_name":"Product 9","product_price":90},{"quantity_of_product":35,"product_id":19,"product_name":"Product 19","product_price":40}]

# ["{\"quantity_of_product\": 1, \"product_id\": 3, \"product_name\": \"Product 3\", \"product_price\": 30}","{\"quantity_of_product\": 33, \"product_id\": 19, \"product_name\": \"Product 19\", \"product_price\": 40}","{\"quantity_of_product\": 1, \"product_id\": 2, \"product_name\": \"Product 2\", \"product_price\": 20}","{\"quantity_of_product\": 1, \"product_id\": 7, \"product_name\": \"Product 7\", \"product_price\": 37}","{\"quantity_of_product\": 1, \"product_id\": 4, \"product_name\": \"Product 4\", \"product_price\": 40}","{\"quantity_of_product\": 3, \"product_id\": 9, \"product_name\": \"Product 9\", \"product_price\": 90}"]}