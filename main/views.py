from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth import login as auth_login

from main.forms import GuestCommentForm, PostForm, UserCommentForm, RegistrationForm
from main.models import Post, Comment

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})


def cat_view(request, tag):
    posts = Post.objects.filter(tags__icontains=tag)
    return render(request, 'home.html', {'posts': posts})
   

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
        return render(request, 'signup.html', {'form': form})



@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by = request.user
            post.save()
            return redirect('post_view', post.pk)

    form = PostForm(request.POST or None)
    return render(request, 'add_post.html', {'form':form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_view', post.pk)
    form = PostForm(request.POST or None, instance=post)
    return render(request, 'add_post.html', {'form':form})


def post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.order_by('-posted_on')
    
    if request.method == "POST":
        if request.user.is_authenticated:
            form = UserCommentForm(request.POST)
        else:
            form = GuestCommentForm(request.POST)

        if form.is_valid():
            if request.user.is_authenticated:
                comment = form.save(commit=False)
                comment.posted_by = request.user
                comment.post = post
                comment.save()
            else:
                message =  form.cleaned_data.get('message')
                poster =  form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                comment = Comment(commented_by=poster, message=message, post=post,email=email)
                comment.save()
            return redirect('post_view', post.pk)
        else:
            if request.user.is_authenticated:
               form = UserCommentForm(request.POST)
            else:
               form = GuestCommentForm(request.POST)
    else:
        post.add_views(request)

        if request.user.is_authenticated:
            form = UserCommentForm(request.POST or None)
        else:
            form = GuestCommentForm(request.POST or None)
    
    return render(request, 'post.html', {'comments':comments,'post': post,'form':form})