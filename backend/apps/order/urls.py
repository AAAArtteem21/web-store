from django.urls import path
from apps.order import views

urlpatterns = [
    path('orders/', views.OrderCreateView.as_view(),name='orders'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(),name='detail order'),
    path('orders/create-from-cart/', views.OrderFromCartView.as_view(),name='order create'),
]   