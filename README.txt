PROJECT SETUP

1) Download the zip file onlineStore and decompress it. 
2) Place it inside a new/separate folder 
3) Go to link and follow steps to install python  version 3.10 : https://www.python.org/downloads/
4) Open the folder created in step2 in terminal and type given below command to create a virtual environment in linux : 
   python -m venv venv 
5) Check,a new folder named 'venv' must be created. This folder will hold all dependencies for your project environment.
6) Activate environment type command in terminal : source venv/bin/activate
7) In your terminal you will now see (venv) written in extreme left of new line, this means venv is now activated.
8) To install all dependencies in this environment type command:
    pip install -r requirements.txt
   the requirements file exists inside onlineStore folder make sure path is correct.
9) Go inside onlineStore folder in terminal and Run command in sequence: 
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver 

Note : The Django server runs by default on port 8000 make sure the port is available and not occupied by some other services.


DATABASE:
The django framework uses sqlite database hence no need to attach separate databases. The database is already populated with dummy entries to test, the app should be functional immediately if all steps are followed correctly. Utilized JWT authentication, hence registration and login will be mandatory to use services. 


API ENDPOINTS:
To test out the APIs tools POSTMAN can be used.
List of endpoints

1) Retrieve list of all products.
   URL: localhost:8000/products/
   METHOD: GET
   PAYLOAD ={}
  
2) Retrieve details of a product.
   URL: localhost:8000/products/<int:id>
   METHOD: GET
   PAYLOAD ={}
   
3) Add product(s) to cart.
   URL: localhost:8000/cart/
   METHOD: POST
   PAYLOAD ={
        'product_id' : int,
        'quantity_of_product' : int,
   }

4) Remove product(s) to cart.
   URL: localhost:8000/cart/
   METHOD: DELETE
   PAYLOAD ={
        'product_id' : int
   }
   
5) Retrieve a user’s cart.
   URL: localhost:8000/cart/
   METHOD: GET
   PAYLOAD ={}
   
6) Register User to use APIs 1 to 5
   URL: localhost:8000/users/register/
   METHOD: POST
   PAYLOAD ={
        'username' : string,
        'password' : string,
   }

6) Login User to use APIs 1 to 5
   URL: localhost:8000/users/login/
   METHOD: POST
   PAYLOAD ={
        'username' : string,
        'password' : string,
   }
   
NOTE : To use APIs other than register and login, ensure that "access token" provided by registration and login process is passed in HTTP request headers parameters.

