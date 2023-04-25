from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('user', views.UserViewSet, 'users')


urlpatterns = [
    path('', include(router.urls)),
    path('oauth-info/', views.OAuthInfo.as_view(), name="oauth"),
    path('forgot-password/', views.ForgotPassword.as_view(), name="forgot"),
    path('reset-password/', views.ResetPassword.as_view(), name="reset"),
    path('activate/', views.ActiveEmail.as_view(), name="activate"),
]