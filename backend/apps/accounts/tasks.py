from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings
from .emails import send_email
from .tokens import password_reset_token, email_verification_token

User = get_user_model()


@shared_task
def send_password_reset_email(user_id):
    user = User.objects.get(pk=user_id)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = password_reset_token.make_token(user)
    link = f"{settings.FRONTEND_URL}/password-reset/{uid}/{token}/"

    print(f"\n🔑 RESET LINK: {link}\n")
    
    send_email(
        subject="Сброс пароля",
        template="emails/password_reset.html",
        context={"user": user, "link": link},
        to_email=user.email,
    )


@shared_task
def send_verification_email(user_id):
    user = User.objects.get(pk=user_id)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    link = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"

    print(f"\n✅ VERIFY LINK: {link}\n")

    send_email(
        subject="Подтверди email",
        template="emails/email_verification.html",
        context={"user": user, "link": link},
        to_email=user.email,
    )


@shared_task
def send_order_confirmation_email(order_id):
    from order.models import Order 
    order = Order.objects.select_related('user').prefetch_related('items__product').get(pk=order_id)

    send_email(
        subject=f"Заказ #{order.id} подтверждён",
        template="emails/order_confirmation.html",
        context={"order": order, "user": order.user},
        to_email=order.user.email,
    )