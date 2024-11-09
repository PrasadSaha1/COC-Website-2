from django.urls import path
from . import views

app_name = 'register'

urlpatterns = [
    path('create_account/', views.create_account, name='create_account'),
    path('', views.create_account, name='create_account'),
    path('login/', views.login_view, name='login'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('confirmation_sent/', views.confirmation_sent, name='confirmation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('change_password_from_email/', views.change_password_from_email, name='change_password_from_email'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    path('forgot_username/', views.forgot_username, name='forgot_username'),
]