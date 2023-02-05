from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse

from main.forms import GuestCommentForm, PostForm, UserCommentForm
from main.models import Post, Comment

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

def cat_view(request, tag):
    posts = Post.objects.filter(tags__contains=tag)
    return render(request, 'home.html', {'posts': posts})
   

# class PostListView(ListView):
#     model = Post
#     context_object_name = "posts"
#     template_name = "home.html"
#     paginate_by = 15

# @method_decorator([login_required], name="dispatch")
# class PostCreateView(CreateView):
#     model = Post
#     form_class = PostForm
#     template_name = "post_add.html"

#     def form_valid(self, form):
#         self.post = form.save(commit=False)
#         self.post.posted_by = self.request.user
#         self.post.save()
#         super().form_valid(form)
#         return redirect('post_view', self.post.pk)


# @method_decorator([login_required], name="dispatch")
# class AnswerUpdateView(UpdateView):
#     model = Answer
#     form_class = AnswerForm
#     template_name = "answer_update.html"
#     pk_url_kwarg = 'answer_pk'
#     context_object_name = 'answer'

#     def form_valid(self, form):
#         self.answer = form.save(commit=False)
#         self.answer.updated_on = timezone.now()
#         self.answer.save()
#         return super().form_valid(form)

#     def get_success_url(self):
#         answer = self.get_object()
#         return reverse('question_detail', kwargs={'pk': answer.question.pk, 'slug': answer.question.slug})



@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by = request.user
            post.save()
            return redirect('post_view', post.pk)
        else:
            PostForm(request.POST)

    form = PostForm()
    return render(request, 'add_post.html', {'form':form})


@method_decorator([login_required], name="dispatch")
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "add_post.html"
    context_object_name = 'post'

    def form_valid(self, form):
        self.post = form.save(commit=False)
        self.post.posted_by = self.request.user
        self.post.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse('post_view', kwargs={'pk': post.pk})


# @login_required
# def edit_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(data=request.POST, post=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.posted_by = request.user
#             post.save()
#             return redirect('post_view', post.pk)
#         else:
#             PostForm(request.POST)

#     form = PostForm()

#     return render(request, 'add_post.html', {'form':form})


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
            form = UserCommentForm()
        else:
            form = GuestCommentForm()
    
    return render(request, 'post.html', {'comments':comments,'post': post,'form':form})