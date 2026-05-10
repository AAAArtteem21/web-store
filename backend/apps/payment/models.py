# apps/payment/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone


class Payment(models.Model):
    """
    Основная модель платежа.
    Привязана к конкретному заказу Order.
    Один заказ — один платёж (OneToOne).
    """
    STATUS_CHOICES = [
        ('pending',    'Ожидает оплаты'),
        ('processing', 'Обрабатывается'),
        ('succeeded',  'Оплачен'),
        ('failed',     'Ошибка'),
        ('cancelled',  'Отменён'),
        ('refunded',   'Возвращён'),
    ]

    order = models.OneToOneField(
        'order.Order',
        on_delete=models.CASCADE,
        related_name='payment',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
    )

    # Сумма и валюта берутся из заказа, но хранятся отдельно
    # на случай если заказ изменится после оплаты
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )

    # Stripe-поля
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)

    # Временные метки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'payments'
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['stripe_session_id']),
            models.Index(fields=['stripe_payment_intent_id']),
        ]

    def __str__(self):
        return f"Payment #{self.id} | Order #{self.order.id} | {self.status}"

    # ── Свойства ──────────────────────────────────────────────

    @property
    def is_paid(self):
        return self.status == 'succeeded'

    @property
    def can_be_refunded(self):
        return self.status == 'succeeded' and self.stripe_payment_intent_id

    # ── Методы смены статуса ──────────────────────────────────

    def mark_as_succeeded(self, payment_intent_id=None):
        """Вызывается из вебхука при checkout.session.completed"""
        self.status = 'succeeded'
        self.paid_at = timezone.now()
        if payment_intent_id:
            self.stripe_payment_intent_id = payment_intent_id
        self.save(update_fields=['status', 'paid_at', 'stripe_payment_intent_id', 'updated_at'])

        # Синхронно обновляем статус заказа
        self.order.status = 'processing'
        self.order.save(update_fields=['status', 'updated_at'])

    def mark_as_failed(self):
        self.status = 'failed'
        self.save(update_fields=['status', 'updated_at'])

    def mark_as_cancelled(self):
        self.status = 'cancelled'
        self.save(update_fields=['status', 'updated_at'])


class Refund(models.Model):
    """
    Возврат средств по платежу.
    Может быть полным или частичным.
    """
    STATUS_CHOICES = [
        ('pending',   'Ожидает'),
        ('succeeded', 'Выполнен'),
        ('failed',    'Ошибка'),
        ('cancelled', 'Отменён'),
    ]

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='refunds',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    stripe_refund_id = models.CharField(max_length=255, blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='initiated_refunds',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'refunds'
        verbose_name = 'Возврат'
        verbose_name_plural = 'Возвраты'
        ordering = ['-created_at']

    def __str__(self):
        return f"Refund #{self.id} | ${self.amount} | Payment #{self.payment.id}"

    @property
    def is_partial(self):
        return self.amount < self.payment.amount

    def mark_as_succeeded(self):
        self.status = 'succeeded'
        self.processed_at = timezone.now()
        self.save(update_fields=['status', 'processed_at'])

        # Обновляем статус платежа
        self.payment.status = 'refunded'
        self.payment.save(update_fields=['status', 'updated_at'])


class WebhookEvent(models.Model):
    """
    Лог всех входящих событий от Stripe.
    Нужен чтобы не обрабатывать одно событие дважды
    и иметь историю для дебага.
    """
    STATUS_CHOICES = [
        ('pending',   'Ожидает'),
        ('processed', 'Обработан'),
        ('failed',    'Ошибка'),
        ('ignored',   'Проигнорирован'),
    ]

    event_id = models.CharField(max_length=255, unique=True)  # stripe event id
    event_type = models.CharField(max_length=100)             # checkout.session.completed и т.д.
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    payload = models.JSONField()          # полный JSON от Stripe
    error_message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'webhook_events'
        verbose_name = 'Webhook-событие'
        verbose_name_plural = 'Webhook-события'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type', 'status']),
        ]

    def __str__(self):
        return f"{self.event_type} | {self.status} | {self.event_id[:20]}..."

    def mark_as_processed(self):
        self.status = 'processed'
        self.processed_at = timezone.now()
        self.save(update_fields=['status', 'processed_at'])

    def mark_as_failed(self, error):
        self.status = 'failed'
        self.error_message = error
        self.processed_at = timezone.now()
        self.save(update_fields=['status', 'error_message', 'processed_at'])