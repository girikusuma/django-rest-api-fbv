from django.urls import path
from .views import category_list, category_detail, product_list, product_detail, login, register
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('categories/', category_list, name='category_list'),
    path('categories/<int:pk>/', category_detail, name='category_detail'),
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
]

urlpatterns = format_suffix_patterns(urlpatterns)