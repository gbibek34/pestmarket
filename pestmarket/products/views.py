from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, ShippingAddress
# Create your views here.


@login_required
def products(request):
    products = Product.objects.all()
    context = {
        'activateproducts': 'active',
        'products': products
    }
    return render(request, 'products/products.html', context)


@login_required
def cart(request):
    customer = request.user
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    items = order.orderitem_set.all()

    context = {
        'activateproducts': 'active',
        'items': items,
        'order': order
    }
    return render(request, 'products/cart.html', context)


@login_required
def checkout(request):
    context = {
        'activateproducts': 'active'
    }
    return render(request, 'products/checkout.html', context)
