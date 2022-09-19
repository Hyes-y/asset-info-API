from django.urls import path, include

urlpatterns = [
    path('users/', include('apps.user.urls')),
    path('accounts/', include('apps.account.urls')),
    path('assets/', include('apps.asset.urls')),
]