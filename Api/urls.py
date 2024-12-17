# Api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet,UserViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'users', UserViewSet) 
router.register(r'clients', ClientViewSet)

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # Authentification par token
    path('users/<int:pk>/update-password/', UserViewSet.as_view({'post': 'update_password'}), name='update_password'),
    path('', include(router.urls)),  # Inclure les routes du router après les routes spécifiques
]