from rest_framework import serializers
from backend.apps.order.models import Order 
 
 
class OrderPaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения заказа перед оплатой.
    Возвращает основные поля + статус оплаты.
    """
    is_paid = serializers.SerializerMethodField()
 
    class Meta:
        model = Order
        fields = [
            "id",
            "total_price",  
            "status",     
            "is_paid",
            "created_at",
        ]
        read_only_fields = fields
 
    def get_is_paid(self, obj):
        return obj.status == "paid"  
 
 
class CheckoutSessionResponseSerializer(serializers.Serializer):
    """
    Ответ после создания Stripe Checkout Session.
    Возвращает URL для редиректа на страницу оплаты Stripe.
    """
    checkout_url = serializers.URLField()
    session_id = serializers.CharField()
 