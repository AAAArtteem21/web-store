from django.urls import path
from backend.apps.cart import views


urlpatterns = [
    path('cart/',views.CartItemListView.as_view(),name='cart'),
    path('add/cart/',views.CartItemAddView.as_view(),name='add-cart'),
    path('del/cart/',views.CartItemDeleteView.as_view(),name='remove-cart'),
]