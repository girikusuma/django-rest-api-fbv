from rest_framework import serializers
from .models import Category, Product
from rest_framework.validators import UniqueValidator

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=200)
    description = serializers.CharField(style={'base_template': 'textarea.html'})

    def create(self, validate_data):
        return Category.objects.create(**validate_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    code = serializers.CharField(max_length=50, validators=[UniqueValidator(queryset=Product.objects.all())])
    name = serializers.CharField(required=True, max_length=200)
    description = serializers.CharField(style={'base_template': 'textarea.html'})

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.category = validated_data.get('name', instance.category)
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance