from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AssetViewSet

router = DefaultRouter()
router.register(r'', AssetViewSet, basename='asset')


urlpatterns = [
    path('', include(router.urls)),
]