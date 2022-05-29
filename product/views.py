from django.db.models import Q
from django.http import Http404
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from .models import Product, Category, Review


class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[:8]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist as e:
            raise Http404 from e

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Product.DoesNotExist as e:
            raise Http404 from e

    def get(self, request, category_slug):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


@api_view(['POST'])
def search(request):
    if query := request.data.get('query', ''):
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def comment(request, category_slug, product_slug):

    product = Product.objects.filter(
        category__slug=category_slug).get(slug=product_slug)

    if request.method == 'POST':
        data = JSONParser().parse(request)

        rating = data['rating']
        content = data['content']

        if content != '':
            reviews = Review.objects.filter(
                created_by=request.user, product=product)

            if reviews.count() > 0:
                review = reviews.first()
                review.rating = rating
                review.content = content
                review.save()
            else:
                review = Review.objects.create(
                    product=product,
                    rating=rating,
                    content=content,
                    created_by=request.user
                )

    serializer = ProductSerializer(product)
    return Response(serializer.data)


class ListReview(APIView):
    def get(self, request, format=None):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class DetailReview(APIView):
    def get_object(self, product_slug, format=None):
        try:
            # return Review.objects.filter(created_by=request.user)
            return Review.objects.filter(product__slug=product_slug)
        except Review.DoesNotExist as e:
            raise Http404 from e

    def get(self, request, product_slug):
        reviews = self.get_object(product_slug)
        # print(reviews)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
