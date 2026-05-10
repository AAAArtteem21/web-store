from django.urls import path
from .views import CreateCheckoutSessionView, OrderPaymentDetailView, StripeWebhookView
 
urlpatterns = [
    path("checkout/<int:order_id>/", CreateCheckoutSessionView.as_view(), name="checkout"),
    path("webhook/", StripeWebhookView.as_view(), name="stripe-webhook"),
    path("order/<int:order_id>/", OrderPaymentDetailView.as_view(), name="order-payment-detail"),
]
 