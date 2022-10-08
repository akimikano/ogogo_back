from djoser.serializers import UserCreatePasswordRetypeSerializer
from rest_framework import serializers
from apps.users.models import User


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class UserCreateSerializer(UserCreatePasswordRetypeSerializer):
    password = serializers.CharField(required=True, write_only=True)
    re_password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 're_password')

