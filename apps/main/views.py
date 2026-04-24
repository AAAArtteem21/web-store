from django.shortcuts import render
from  rest_framework import generics,permissions,status,filters
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import Product,ProductImage,ProductSize,Size,Category
from .serializers import ProductDetailSerializer,CategorySerializer
import django_filters
from .filters import ProductFilter

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.select_related('category').prefetch_related('product_sizes__size','images').annotate(likes_count=Count('likes')).all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name','description','color']
    ordering_fields = ['price','created_at','name']
    ordering = ['-created_at']


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.select_related('category').prefetch_related('product_sizes__size','images').all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_like(request, slug):
    product = get_object_or_404(
        Product.objects.annotate(likes_count=Count('likes')),
        slug=slug
    )
    user = request.user

    if user in product.likes.all():
        product.likes.remove(user)
        liked=False
    else:
        product.likes.add(user)
        liked = True

    return Response({
        'liked': liked,
        'likes_count': product.likes_count
    })