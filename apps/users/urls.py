from django.urls import path, include
from rest_framework_simplejwt import views
from apps.users.views import (
    CreateTokenPairView,
    RegisterView
)

urlpatterns = [
    path('', include('djoser.urls')),
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
]