from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post


def home(request):
    return HttpResponse('<h1>Blog Home</h1>')

def about(request):
    return HttpResponse('<h1>Blog About</h1>')

def post_list(request):
    """ function-based view for blog home page """
    posts = Post.objects.filter(status='published').order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, 'home.html', context)

def post_detail(request, slug):
    """ function-based view for post detail page """
    post = get_object_or_404(Post, slug=slug, status='published')
    context = {
        'post': post 
    }
    return render(request, 'post_detail.html', context)
