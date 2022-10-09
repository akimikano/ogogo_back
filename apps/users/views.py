from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework import viewsets, views, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from apps.users.models import User
from rest_framework.authtoken.models import Token
from .serializers import *
from rest_framework.generics import (
    CreateAPIView
)
from djoser.views import TokenCreateView
from djoser.conf import settings
from djoser import signals, utils


class CreateTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCreateSerializer


class UserView(viewsets.GenericViewSet,
               mixins.CreateModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserUpdateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token = Token.objects.create()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CustomLogin(TokenCreateView):
    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        data = token_serializer_class(token).data
        data.update({
            'user_type': serializer.user.type
        })
        return Response(
            data=data, status=status.HTTP_200_OK
        )








