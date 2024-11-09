from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('password_reset/', views.reset_password, name='register'),
    # Add other URL patterns for registration if necessary
]