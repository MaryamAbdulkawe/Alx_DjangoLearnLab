from django.urls import path
from . import views

urlpatterns = [
    # Posts
    path('', views.PostListCreateView.as_view(), name='post_list_create'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('feed/', views.feed, name='feed'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    
    # Comments
    path('<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment_list_create'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
]