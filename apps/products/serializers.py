from rest_framework import serializers

from apps.products.models import Product


class ProductCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_title', 'product_description', 'price']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_title', 'price', 'seller']