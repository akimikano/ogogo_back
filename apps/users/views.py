from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from apps.users.models import User


class CreateTokenPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            update_last_login(User, user)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


