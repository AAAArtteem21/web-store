from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .import views
from .views import (
    RegisterView, LoginView, ProfileView,
    ChangePasswordView, logout_view,
    PasswordResetRequestView, VerifyEmailView, PasswordResetConfirmView
)

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('change-password/',views.ChangePasswordView.as_view(),name='change-password'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token-refresh'),
    path('password-reset/', PasswordResetRequestView.as_view()),
    path('password-reset/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view()),
    path('verify-email/<str:uidb64>/<str:token>/', VerifyEmailView.as_view()),

]