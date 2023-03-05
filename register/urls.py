from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('forgot-password/', views.forgot_password, name="forgot_password"),
    path('reset-user-password/<str:uidb64>/<str:token>/', views.reset_password, name="custom_password_reset_confirm"),

]
