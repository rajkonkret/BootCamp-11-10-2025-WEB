from django.urls import path

from .views import home, list_posts

urlpatterns = [
    path('', home, name="home"),  # endpoint '/'
    path('posts/', list_posts, name="posts")
]
