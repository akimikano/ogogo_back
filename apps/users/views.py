from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from apps.users.models import User
from .serializers import MyTokenObtainPairSerializer


class CreateTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny)
    serializer_class = MyTokenObtainPairSerializer

