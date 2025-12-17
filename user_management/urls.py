from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignupView, LoginView, ProfileView, LogoutView, AddressCreateAPIView, AddressPartialDetailsAPIView
urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path("address", AddressCreateAPIView.as_view(), name="profile_add"),
    path("address/<int:pk>", AddressPartialDetailsAPIView.as_view(), name="Profile_update"),

]
