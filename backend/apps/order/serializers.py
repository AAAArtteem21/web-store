from rest_framework import serializers
from .models import Order,OrderItem
from apps.cart.models import Cart
import uuid


        

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.main_image', read_only=True)
    size_name = serializers.CharField(source='size.size.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'size', 'size_name', 'quantity', 'price']
        read_only_fields = ['price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['id','first_name','last_name','email','company',
                  'address1','address2','city','country','province','postal_code',
                  'phone','special_instructions','total_price','status','stripe_payment_intent_id',
                  'created_at','updated_at','items']
        read_only_fields = ['status','stripe_payment_intent_id','total_price']

    def validate(self,data):
        for item in data.get('items',[]):
            product = item['product']
            if product.stock < item['quantity']:
                raise serializers.ValidationError(
                    f"Prodcut {product.name} don`t have"
                )
        return data

    def create(self,validated_data):
        request = self.context['request']
        user = request.user
        items_data = validated_data.pop('items')

        order = Order.objects.create(user=user,total_price=0,**validated_data)

        total_price = 0
        for item in items_data:
            order_item = OrderItem.objects.create(
                order=order,product_item=['product'],
                size=item.get('siez'),
                quantity=item['quantity'],
                price=item['product'].price
            )
            total_price += order_item.price * order_item.quantity

            product = order_item.product
            product.stock -= order_item.quantity
            product.save()


        
        order.total_price = total_price
        order.save()

        Cart.objects.filter(user=user).delete()

        return order
