from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializers import UserSerializer
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from .authentication import JwtAuthenticationCookie
from user.models import CustomUser


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = CustomUser.objects.filter(
            email=serializer.data['email']).first()
        if user is None:
            raise exceptions.AuthenticationFailed("User Not saved")
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        response = Response(serializer.data)
        response.set_cookie(key="access", value=access_token,
                            httponly=False)
        response.set_cookie(key="refresh", value=refresh,
                            httponly=False)
        return response


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        print(request)
        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Incorrect Password")

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response()
        response.set_cookie(key="access", value=access_token,
                            httponly=False)
        response.set_cookie(key="refresh", value=refresh,
                            httponly=False)
        response.data = {
            'message': 'success'
        }

        return response


class UserProfileAPIView(APIView):
    authentication_classes = [JwtAuthenticationCookie]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = UserSerializer(user).data
        return Response(data=data)


class LogoutAPIView(APIView):
    authentication_classes = [JwtAuthenticationCookie]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = Response()
        response.delete_cookie("access")
        response.delete_cookie("refresh")

        response.data = {
            'message': 'Logout successful'
        }
        return response
