from django.contrib import admin
from django.utils.html import format_html
from .models import Payment, Refund, WebhookEvent


class RefundInline(admin.TabularInline):
    model = Refund
    extra = 0
    readonly_fields = ('amount', 'status', 'stripe_refund_id', 'created_at', 'processed_at')
    fields = ('amount', 'reason', 'status', 'created_by')
    can_delete = False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_link', 'user', 'amount', 'currency', 'status_display', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('user__username', 'user__email', 'stripe_session_id', 'stripe_payment_intent_id')
    readonly_fields = ('created_at', 'updated_at', 'paid_at', 'is_paid', 'can_be_refunded')
    raw_id_fields = ('user', 'order')
    inlines = [RefundInline]

    fieldsets = (
        (None, {
            'fields': ('order', 'user', 'amount', 'currency', 'status')
        }),
        ('Stripe', {
            'fields': ('stripe_session_id', 'stripe_payment_intent_id'),
            'classes': ('collapse',)
        }),
        ('Статус', {
            'fields': ('is_paid', 'can_be_refunded'),
            'classes': ('collapse',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at', 'paid_at'),
            'classes': ('collapse',)
        }),
    )

    def order_link(self, obj):
        from django.urls import reverse
        url = reverse('admin:order_order_change', args=[obj.order.pk])
        return format_html('<a href="{}">Order #{}</a>', url, obj.order.id)
    order_link.short_description = 'Заказ'

    def status_display(self, obj):
        colors = {
            'succeeded': 'green', 'failed': 'red',
            'pending': 'orange', 'processing': 'blue',
            'cancelled': 'gray', 'refunded': 'purple',
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color:{};font-weight:bold;">{}</span>', color, obj.status.upper())
    status_display.short_description = 'Статус'


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment', 'amount', 'status', 'is_partial', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('payment__id', 'stripe_refund_id')
    readonly_fields = ('created_at', 'processed_at', 'is_partial')
    raw_id_fields = ('payment', 'created_by')


@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_type', 'status', 'event_id', 'created_at')
    list_filter = ('status', 'event_type', 'created_at')
    search_fields = ('event_id', 'event_type')
    readonly_fields = ('event_id', 'event_type', 'payload', 'created_at', 'processed_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser