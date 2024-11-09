from django.contrib import admin
from django.urls import path, include
from register import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', include('register.urls')),  # Include the app's URLs
    path('', include("main.urls")),
    path('', include("django.contrib.auth.urls")),
    path('activate/<uidb64>/<token>/', v.activate, name='activate'),
]