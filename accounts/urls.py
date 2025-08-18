# accounts/urls.py
from django.urls import path
from . import views
from .views import create_superuser

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path("create-superuser/", create_superuser),
]
    
    
