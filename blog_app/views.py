from django.shortcuts import render
from .models import BlogPost

def home(request):
    posts = BlogPost.objects.all()
    return render(request, 'home.html', {'posts': posts})

def post_detail(request, pk):
    post = BlogPost.objects.get(pk=pk)
    return render(request, 'post_detail.html', {'post': post})
