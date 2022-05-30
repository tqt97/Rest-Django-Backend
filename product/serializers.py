from rest_framework import serializers
from .models import Category, Product, Review


# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = ('rating', 'content', 'created_by', 'created_at')


class ProductSerializer(serializers.ModelSerializer):

    # items = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'get_absolute_url', 'description','image',
                  'price', 'get_image', 'get_thumbnail', 'get_rating', 'items', 'get_name')


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'get_absolute_url', 'products')


class ReviewSerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Review
        fields = ('get_product', 'rating', 'content',
                  'get_user', 'created_at','get_date')
