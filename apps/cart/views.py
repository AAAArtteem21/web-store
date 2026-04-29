from django.shortcuts import render
from  rest_framework import generics,permissions,status,filters
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import CartItem,Cart
from .serializer import CartSerializer,CartItemSerializer
import django_filters
from rest_framework.views import APIView



class CartItemListView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(
            cart__user=self.request.user
        ).select_related('product', 'product_size').order_by('added_at')


class CartItemAddView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        product_id = self.request.data.get('product_id')
        quantity = int(self.request.data.get('quantity', 1))

        # если уже есть — обновляем количество
        item = CartItem.objects.filter(
            cart=cart, 
            product_id=product_id
        ).first()

        if item:
            item.quantity += quantity
            item.save()
        else:
            serializer.save(cart=cart)


class CartItemDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            return Response({'message': 'count product changed'})
        item.delete()
        return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)