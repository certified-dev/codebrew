from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required

from main.forms import GuestCommentForm, PostForm, UserCommentForm
from main.models import Post, GuestComment

def home(request):
    posts = Post.objects.all().order_by('-posted_on')
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


@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by = request.user
            post.save()
            return redirect('post_view', post.pk)

    form = PostForm()
    return render(request, 'add_post.html', {'form':form})

def post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.guest_comments.order_by('-posted_on') + post.user_comments.order_by('-posted_on')
    
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
                message =  message=form.cleaned_data.get('message')
                poster =  message=form.cleaned_data.get('name')
                comment = GuestComment(posted_by=poster, message=message, post=post)
                comment.save()
    else:
        session_key = 'viewed_question_{}'.format(post.pk)
        if not request.session.get(session_key, False):
            post.views += 1
            post.save()
            request.session[session_key] = True
    
        if request.user.is_authenticated:
            form = UserCommentForm()
        else:
            form = GuestCommentForm()
    
    return render(request, 'post.html', {'comments':comments,'form':form})