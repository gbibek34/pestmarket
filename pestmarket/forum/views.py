from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def forum(request):
    context = {
        'posts': Post.objects.all(),
        'activateforum': 'active'
    }
    return render(request, 'forum/forum.html', context)
