from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
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


@login_required
def post_create(request):
    """" create new blog """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # save the form but don't commit to database yet
            post = form.save(commit=False)
            # assign the current user as author
            post.author = request.user
            # now save to database
            post.save()
            return redirect('home')
    else:
        # GET request - show empty form
        form = PostForm()
    context = {
        'form' : form
    }
    return render(request, 'post_form.html', context)


@login_required
def post_update(request, slug):
    """
    edit on an existing post 
    only author can edit their own posts 
    """
    post = get_object_or_404(Post, slug=slug, author=request.user)

    if request.method == 'POST':
        # pass existing post instance to form
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', slug=post.slug)
    else:
        # GET request - pre-fill form with existing data
        form = PostForm(instance=post)
    context = {
        'form': form,
        'post': post
    }
    return render(request, 'post_form.html', context)


@login_required
def post_delete(request, slug):
    """
    delete post blog
    only author can delete their own posts
    """
    post = get_object_or_404(Post, slug=slug, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    context ={
        'post': post
    }
    return render('post_confirm_delete.html', context)


def register_view(request):
    """ User registration """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})


def login_view(request):
    """ User login """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})


def logout_view(request):
    """ User logout """
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return render(request, 'authentication/logout.html')
