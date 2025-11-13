from django.urls import path
from .views import UsuarioView, CustomTokenObtainPairView, CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UsuarioView.as_view(), name='user_profile'),
    path('createuser/', CreateUserView.as_view(), name='create-user'),
]
