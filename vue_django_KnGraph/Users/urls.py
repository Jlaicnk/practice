from django.urls import path
from .views import RegisterView, LoginView, LogoutView
from .views import UserPreferencesView
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    path('api/user_preferences/', UserPreferencesView.as_view(), name='user_preferences'),
    path('api/alterUserPreferences/',views.alterUserPreferences, name='alterUserPreferences'),
]