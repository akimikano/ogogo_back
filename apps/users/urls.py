from django.urls import path, include
from rest_framework_simplejwt import views
from apps.users.views import (
    CreateTokenPairView,
    RegisterView, CustomLogin
)

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/token/custom_login/', CustomLogin.as_view(), name="custom_login"),
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
]