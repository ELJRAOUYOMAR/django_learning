from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm

# def home(request):
#     return HttpResponse('<h1>Blog Home</h1>')

# def about(request):
#     return HttpResponse('<h1>Blog About</h1>')

def post_list(request):
    """ Display list of published blog posts with pagination """
    posts_list = Post.objects.filter(status='published').order_by('-created_at')

    # pagination
    paginator = Paginator(posts_list, 4)  # 4 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'is_paginated': posts.has_other_pages(),
        'page_obj': posts
    }

    return render(request, 'home.html', context)

def post_detail(request, slug):
    """ function-based view for post detail page """
    post = get_object_or_404(Post, slug=slug, status='published')
    context = {
        'post': post 
    }
    return render(request, 'post_detail.html', context)
