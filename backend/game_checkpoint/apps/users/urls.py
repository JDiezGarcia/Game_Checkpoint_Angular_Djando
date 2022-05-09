from django.urls import path
from .views import CookieTokenRefreshView, CookieTokenObtainPairView, ProfileView, RegisterViewSet, LogoutView

urlpatterns = [
    path('auth/login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='user_logout'),
    path('auth/register/', RegisterViewSet.as_view({'post': 'create'}), name='user_register'),
    path(r'profiles/<str:username>/', ProfileView.as_view({'get': 'details'}), name='user_profile')
]
