from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TransactionCheckViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'validation', TransactionCheckViewSet, basename='transaction-validation')
router.register(r'', TransactionViewSet, basename='transaction')


urlpatterns = [
    path('', include(router.urls)),
]