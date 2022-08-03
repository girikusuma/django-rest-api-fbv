import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import Category, Product
from django.contrib.auth.models import User
from .serializers import CategorySerializer, ProductSerializer

# Create your tests here.
cln = APIClient()

class CategoryListTest(APITestCase):

    def setUp(self):

        self.user_data = {
            "username": "giri",
            "password": "pasword"
        }

        self.res_register = self.client.post(reverse('register'), self.user_data, format="json")
        self.assertEqual(self.res_register.status_code, status.HTTP_201_CREATED)

        self.res_login = self.client.post(reverse('login'), self.user_data, format="json")
        self.assertEqual(self.res_login.status_code, status.HTTP_200_OK)

        Category.objects.create(name="Electronic", description="That things about electronic")
        Category.objects.create(name="Fashion", description="That things about fashion")
        Category.objects.create(name="Food", description="That things about food")

        return super().setUp()
    
    def test_get_list_categories(self):  
        cln.credentials(HTTP_AUTHORIZATION="Token " + str(self.res_login.data['token']))
        response = cln.get(reverse('category_list'))
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.data["data"], serializer.data)
    
    def test_get_list_products(self):      
        cln.credentials(HTTP_AUTHORIZATION="Token " + str(self.res_login.data['token']))
        response = cln.get(reverse('product_list'))
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data["data"], serializer.data)

