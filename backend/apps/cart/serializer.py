from rest_framework import serializers
from .models import Cart,CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_image = serializers.ImageField(source='product.main_image', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_category = serializers.CharField(source='product.category.name', read_only=True)
    size_name = serializers.CharField(source='product_size.size.name', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_name', 'product_price',
            'product_image', 'product_slug', 'product_category',
            'product_size', 'size_name', 'quantity', 'total_price', 'added_at'
        ]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    subtotal= serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    class Meta:
        model = Cart
        fields = ['id','session_key','items','total_items','subtotal','created_at','updated_at']


