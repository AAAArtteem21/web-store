from django.urls import path
from . import views

urlpatterns = [
    path('category/',views.CategoryListView.as_view(),name='Category-list'),
    path('category/<slug:slug>/',views.CategoryDetailView.as_view(),name='Category-detail'),
    path('',views.ProductListView.as_view(),name='product-list'),
    path('<slug:slug>/',views.ProductDetailView.as_view(),name='product-detail'),
    path('<slug:slug>/like/',views.toggle_like.as_view(),name='product-like'),

]