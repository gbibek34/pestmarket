from django.shortcuts import render
from .models import Post, Like
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CreatePostForm

# Create your views here.


@login_required
def forum(request):
    context = {
        'posts': Post.objects.all(),
        'activateforum': 'active'
    }
    return render(request, 'forum/forum.html', context)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'forum/forum.html'
    context_object_name = 'posts'
    ordering = ['-date_time']

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['activateforum'] = 'active'
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'forum/post.html'
    form_class = CreatePostForm

    def get_context_data(self, **kwargs):
        post = Post.objects.filter(pk=self.kwargs['pk']).first()
        likes = Like.objects.filter(post=self.kwargs['pk'], liked=True).count()
        liked_post = Like.objects.filter(
            post=self.kwargs['pk'], user=self.request.user).first()
        if liked_post != None:
            liked_post = liked_post.liked
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['liked_post'] = liked_post
        context['post'] = post
        context['likes'] = likes
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = {}
        current_post = Post.objects.filter(pk=self.kwargs['pk']).first()
        print(request.POST)
        if 'like_post' in request.POST:
            # current_post.like_post()
            liked_post = Like.objects.filter(
                post=current_post, user=self.request.user).first()
            if liked_post == None:
                liked_post = Like.objects.create(
                    post=current_post, user=self.request.user)
                liked_post.is_liked()
            else:
                liked_post.is_liked()
        if 'dislike_post' in request.POST:
            # current_post.dislike_post()
            liked_post = Like.objects.filter(
                post=current_post, user=self.request.user).first()
            liked_post.not_liked()
        return render(request, self.template_name, self.get_context_data(**context))


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'forum/post_delete.html'
    success_url = '/forum/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
