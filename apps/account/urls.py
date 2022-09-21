from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AccountViewSet

router = DefaultRouter()
router.register(r'', AccountViewSet, basename='account')


urlpatterns = [
    path('', include(router.urls)),
]