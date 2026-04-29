from django.urls import path
from apps.cart import views


urlpatterns = [
    path('cart/',views.CartItemView.as_view(),name='cart'),
    path('add/cart/',views.AddToCartView.as_view(),name='add-cart'),
    path('del/cart/',views.RemoveToCartView.as_view(),name='remove-cart'),
]