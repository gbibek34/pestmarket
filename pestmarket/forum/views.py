from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Post, Comment
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CreatePostForm, CreateCommentForm

# Create your views here.


@login_required
def forum(request):
    context = {
        'posts': Post.objects.all(),
        'activateforum': 'active'
    }
    return render(request, 'forum/forum.html', context)


@login_required
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post-view', args=[str(pk)]))


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
    fields = ['body']

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        get_post = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = get_post.total_likes()
        total_comments = get_post.total_comments()
        liked = False
        if get_post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['activateforum'] = 'active'
        context['total_likes'] = total_likes
        context['total_comments'] = total_comments
        context['liked'] = liked
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['body']
    template_name = 'forum/comment.html'
    success_url = '/forum/{}'

    def form_valid(self, form):
        form.instance.name = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(PostCommentView, self).get_context_data(**kwargs)
        post = self.kwargs['pk']
        context['post'] = post
        return context

    def get_success_url(self, **kwargs):
        return reverse("post-view", kwargs={'pk': self.kwargs['pk']})


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
