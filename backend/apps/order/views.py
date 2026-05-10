from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderItemSerializer,OrderSerializer
from .models import Order,OrderItem
from apps.cart.models import Cart,CartItem

class OrderCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes =[IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
class OrderFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart None'}, status=404)
        
        if not cart.items.exists():
            return Response({'error': 'Cart clear'}, status=400)

        user = request.user
        order = Order.objects.create(
            user=user,
            first_name=request.data.get('first_name') or user.first_name or user.username,
            last_name=request.data.get('last_name') or user.last_name or '',
            email=request.data.get('email') or user.email or '',
            total_price=0
        )

        total = 0
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                size=item.product_size,
                quantity=item.quantity,
                price=item.product.price
            )
            total += item.product.price * item.quantity

        order.total_price = total
        order.save()
        cart.clear()

        return Response({'status': 'order created', 'order_id': order.id})