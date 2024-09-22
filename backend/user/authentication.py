from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication


class JwtAuthenticationCookie(JWTAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access')
        print(token)
        if not token:
            return None
        try:
            validated_token = self.get_validated_token(token)
            print(validated_token)
            user = self.get_user(validated_token)
        except exceptions.AuthenticationFailed as e:
            raise e
        except Exception:
            raise exceptions.AuthenticationFailed("Unauthorized")

        return (user, validated_token)
