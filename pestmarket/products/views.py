from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, ShippingAddress
from .forms import CheckoutForm
from django.http import JsonResponse
import json
# Create your views here.


@login_required
def products(request):
    products = Product.objects.all()
    customer = request.user
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartitems = order.get_cart_items

    context = {
        'activateproducts': 'active',
        'products': products,
        'cartitems': cartitems
    }
    return render(request, 'products/products.html', context)


@login_required
def cart(request):
    customer = request.user
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartitems = order.get_cart_items

    if request.method == 'POST':
        checkoutform = CheckoutForm(request.POST)
        if checkoutform.is_valid():
            checkoutform.save()
            messages.success(request, f'Order Placed Successfully')
            return redirect('/products/')
    else:
        checkoutform = CheckoutForm(request.POST)

    context = {
        'activateproducts': 'active',
        'items': items,
        'order': order,
        'checkoutform': checkoutform,
    }
    return render(request, 'products/cart.html', context)


@login_required
def checkout(request):
    context = {
        'activateproducts': 'active'
    }
    return render(request, 'products/checkout.html', context)


@login_required
def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user
    product = Product.objects.get(id=productId)
    order, create = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)
