from urllib import response
from django.http import HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create your views here.
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    User.objects.create(username=username, password=make_password(password))
    return Response(status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response(data={'token': token.key},
                    status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_list(request, format=None):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        response = {
            'code': status.HTTP_200_OK,
            'status': 'List categories',
            'data': serializer.data,
        }
        return Response(data=response, content_type="application/json", status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'code': status.HTTP_201_CREATED,
                'status': 'Category created',
                'data': serializer.data,
            }
            return Response(response)
        response = {
            'code': status.HTTP_400_BAD_REQUEST,
            'status': serializer.errors,
            'data': [],
        }
        return Response(response)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_detail(request, pk, format=None):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        response = {
            'code': status.HTTP_400_BAD_REQUEST,
            'message': "Category does not exists",
        }
        return HttpResponse(response)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        response = {
            'code': status.HTTP_200_OK,
            'status': 'Get category',
            'data': serializer.data,
        }
        return Response(response)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(category, data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'code': status.HTTP_200_OK,
                'status': 'Category updated',
                'data': serializer.data,
            }
            return Response(response)
    elif request.method == 'DELETE':
        category.delete()
        response = {
            'code': status.HTTP_204_NO_CONTENT,
            'status': 'Category destroy',
        }
        return Response(response)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def product_list(request, format=None):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        response = {
            'code': status.HTTP_200_OK,
            'status': 'List products',
            'data': serializer.data,
        }
        return Response(response)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'code': status.HTTP_201_CREATED,
                'status': 'Product created',
                'data': serializer.data,
            }
            return Response(response)
        response = {
            'code': status.HTTP_400_BAD_REQUEST,
            'status': serializer.errors,
            'data': [],
        }
        return Response(response)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def product_detail(request, pk, format=None):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        response = {
            'code': status.HTTP_400_BAD_REQUEST,
            'message': "Product does not exists",
        }
        return HttpResponse(response)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        response = {
            'code': status.HTTP_200_OK,
            'status': 'Get product',
            'data': serializer.data,
        }
        return Response(response)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(product, data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'code': status.HTTP_200_OK,
                'status': 'Product updated',
                'data': serializer.data,
            }
            return Response(response)
    elif request.method == 'DELETE':
        product.delete()
        response = {
            'code': status.HTTP_204_NO_CONTENT,
            'status': 'Product destroy',
        }
        return Response(response)