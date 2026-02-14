from django.urls import path

from .views import home, list_posts, get_post

urlpatterns = [
    path('', home, name="home"),  # endpoint '/'
    path('posts/', list_posts, name="posts"),
    path('posts/<int:post_id>/', get_post),
]
