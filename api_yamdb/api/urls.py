from django.urls import path, include
from .views import signup
from rest_framework import routers

app_name = 'api'

urlpatterns = [
    # path('v1/', include(router.urls)),
    # path('v1/', include('djoser.urls')),
    # path('v1/', include('djoser.urls.jwt')),
    path('v1/auth/signup/', signup),
]
