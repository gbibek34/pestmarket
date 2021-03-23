from django.shortcuts import render

# Create your views here.


def forum(request):
    context = {
        'activateforum': 'active'
    }
    return render(request, 'forum/forum.html', context)
