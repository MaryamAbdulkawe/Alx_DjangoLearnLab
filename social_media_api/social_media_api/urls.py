"""
URL configuration for social_media_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import render

def api_root(request):
    """API root endpoint showing available endpoints"""
    api_urls = {
        'message': 'Welcome to Social Media API',
        'version': '1.0',
        'endpoints': {
            'authentication': {
                'register': '/api/accounts/register/',
                'login': '/api/accounts/login/',
                'profile': '/api/accounts/profile/',
            },
            'users': {
                'list_users': '/api/accounts/users/',
                'follow_user': '/api/accounts/follow/<user_id>/',
                'unfollow_user': '/api/accounts/unfollow/<user_id>/',
            },
            'posts': {
                'list_posts': '/api/posts/',
                'create_post': '/api/posts/',
                'post_detail': '/api/posts/<post_id>/',
                'user_feed': '/api/posts/feed/',
                'like_post': '/api/posts/<post_id>/like/',
            },
            'comments': {
                'post_comments': '/api/posts/<post_id>/comments/',
                'create_comment': '/api/posts/<post_id>/comments/',
            },
            'admin': '/admin/',
        }
    }
    return JsonResponse(api_urls, json_dumps_params={'indent': 2})

def home_view(request):
    """Home page showing project information"""
    return render(request, 'home.html')

urlpatterns = [
    path('', home_view, name='home'),
    path('api/', api_root, name='api_root'),
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/posts/', include('posts.urls')),
]
