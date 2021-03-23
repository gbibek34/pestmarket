from django.shortcuts import render

# Create your views here.


def products(request):
    context = {
        'activateproducts': 'active'
    }
    return render(request, 'products/products.html', context)
