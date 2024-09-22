from django.urls import path
from .views import LoginAPIView, LogoutAPIView, RegisterAPIView, UserProfileAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('user/register/', RegisterAPIView.as_view()),
    path('user/info/', UserProfileAPIView.as_view()),
    path('user/logout/', LogoutAPIView.as_view()),
]
