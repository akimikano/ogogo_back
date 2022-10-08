from django.urls import path, include
from rest_framework_simplejwt import views
from apps.users.views import CreateTokenPairView

urlpatterns = [
    path('', include('djoser.urls')),
    path("jwt/create/", CreateTokenPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", views.TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", views.TokenVerifyView.as_view(), name="jwt-verify"),
]