import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
 
from backend.apps.order.models import Order  # поменяй путь если у тебя другой
from .serializers import CheckoutSessionResponseSerializer, OrderPaymentSerializer
 
stripe.api_key = settings.STRIPE_SECRET_KEY
 
 
class CreateCheckoutSessionView(APIView):
    """
    POST /api/payments/checkout/<order_id>/
 
    Создаёт Stripe Checkout Session для конкретного заказа.
    Возвращает checkout_url — на него нужно сделать редирект на фронте.
    """
    permission_classes = [IsAuthenticated]
 
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
 
        # Не даём повторно оплатить уже оплаченный заказ
        if order.status == "paid":
            return Response(
                {"detail": "Этот заказ уже оплачен."},
                status=status.HTTP_400_BAD_REQUEST,
            )
 
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",  # поменяй на свою валюту
                            "product_data": {
                                "name": f"Заказ #{order.id}",
                            },
                            # Stripe принимает сумму в центах → умножаем на 100
                            "unit_amount": int(order.total_price * 100),
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                # После успешной оплаты Stripe редиректит сюда
                success_url=settings.STRIPE_SUCCESS_URL + f"?order_id={order.id}",
                # При отмене — сюда
                cancel_url=settings.STRIPE_CANCEL_URL + f"?order_id={order.id}",
                # Сохраняем order_id в метаданных — пригодится в вебхуке
                metadata={"order_id": str(order.id)},
            )
        except stripe.error.StripeError as e:
            return Response(
                {"detail": f"Ошибка Stripe: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
 
        serializer = CheckoutSessionResponseSerializer(
            {"checkout_url": session.url, "session_id": session.id}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 
 
class StripeWebhookView(APIView):
    """
    POST /api/payments/webhook/
 
    Принимает события от Stripe.
    Обрабатывает checkout.session.completed → помечает заказ как оплаченный.
 
    ВАЖНО: этот эндпоинт должен быть ИСКЛЮЧЁН из CSRF и аутентификации.
    """
    authentication_classes = []
    permission_classes = []
 
    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
 
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            # Невалидный payload
            return Response(
                {"detail": "Invalid payload"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except stripe.error.SignatureVerificationError:
            # Подпись не совпала — возможна подделка
            return Response(
                {"detail": "Invalid signature"},
                status=status.HTTP_400_BAD_REQUEST,
            )
 
        # ── Обработка событий ──────────────────────────────────
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            order_id = session.get("metadata", {}).get("order_id")
 
            if order_id:
                Order.objects.filter(id=order_id).update(status="paid")
                # Сюда можно добавить: отправку email, создание Invoice и т.д.
 
        # Stripe ожидает 200 в ответ — иначе будет повторять запрос
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
 
 
class OrderPaymentDetailView(APIView):
    """
    GET /api/payments/order/<order_id>/
 
    Возвращает информацию о заказе и статусе оплаты.
    Удобно использовать на success-странице после редиректа от Stripe.
    """
    permission_classes = [IsAuthenticated]
 
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        serializer = OrderPaymentSerializer(order)
        return Response(serializer.data)
 