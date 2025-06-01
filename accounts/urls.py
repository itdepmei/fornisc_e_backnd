from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('users/', UserManagementView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserManagementView.as_view(), name='user-detail'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('change-password/', AdminChangeUserPasswordView.as_view(), name='admin-change-password'),
    path("register-device/" , DeviceView.as_view() , name="register-device"),
    path("toggle-activity/<int:pk>/", ToggleUserActivity.as_view(), name="toggle-user-activity"),
]

