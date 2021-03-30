from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def products(request):
    context = {
        'activateproducts': 'active'
    }
    return render(request, 'products/products.html', context)
