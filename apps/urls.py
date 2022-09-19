from django.urls import path, include

urlpatterns = [
    path('accounts/', include('apps.account.urls')),
    path('assets/', include('apps.asset.urls')),
]