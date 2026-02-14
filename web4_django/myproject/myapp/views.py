from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Post


# Create your views here.
# def home(request):
#     return HttpResponse("Witaj w mojej aplikacji Django")

def home(request):
    return render(request, "myapp/index.html", {"message": "Django działa!"})


# def list_posts(request):
#     posts = Post.objects.all().order_by("-created_at")
#
#     data = [
#         {
#             "id": post.id,
#             "title": post.title,
#             "content": post.content,
#             "created_at": post.created_at,
#         }
#         for post in posts
#     ]
#
#     return JsonResponse(data, safe=False)

def list_posts(request):
    posts = Post.objects.all().order_by("-created_at")

    return render(
        request,
        "myapp/posts.html",
        {"posts": posts}
    )
