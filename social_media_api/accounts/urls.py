from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts_root, name='accounts_root'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('profile/', views.profile, name='profile'),
    path('users/', views.list_users, name='list_users'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
]