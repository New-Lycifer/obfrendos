from django.urls import path, include
from . import views
from .views import custom_login, profile

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('login/', custom_login, name='login'),
    path('profile/<int:user_id>/', profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
]