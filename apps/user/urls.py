from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView


urlpatterns = [
    path('login', TokenObtainPairView.as_view()),
    path('login/refresh', TokenRefreshView.as_view()),
    path('login/verify', TokenVerifyView.as_view()),
]