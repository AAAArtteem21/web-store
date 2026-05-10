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
        product_id = self.request.data.get('product')
        product_size_id = self.request.data.get('product_size')
        quantity = int(self.request.data.get('quantity', 1))

        item = CartItem.objects.filter(
            cart=cart,
            product_id=product_id,
            product_size_id=product_size_id
        ).first()

        if item:
            item.quantity += quantity
            item.save()
        else:
            serializer.save(cart=cart)

class CartItemDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        item_id = request.data.get('item_id')
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
            item.delete()
            return Response({'message': 'deleted'}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    

class CartItemUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
    
    def update(self,request,*args,**kwargs):
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')
        try:
            item = CartItem.objects.get(id=item_id,cart__user=request.user)
            if quantity < 1:
                item.delete()
                return Response({'message':'deleted'})
            item.quantity = quantity
            item.save()
            return Response(CartItemSerializer(item).data)
        except CartItem.DoesNotExist:
            return Response({'error':'Not found'},status=status.HTTP_404_NOT_FOUND)