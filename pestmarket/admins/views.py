from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product, Order, OrderItem, ShippingAddress
from django.contrib.auth.models import User
from .forms import AddProductForm, UpdateProductForm

# Create your views here.


def dashboard(request):
    context = {}
    context['product_form'] = AddProductForm
    context['product_update_form'] = UpdateProductForm
    products = Product.objects.all()
    products_count = Product.objects.count()
    user_count = User.objects.count()
    orders_count = ShippingAddress.objects.count()
    if request.method == 'POST':
        if 'add_product' in request.POST:
            product_form = AddProductForm(request.POST, request.FILES)
            if product_form.is_valid():
                product_form.save()
                messages.success(request, f'Product Added')
                return redirect('/admins/dashboard/')
        else:
            product_form = AddProductForm(request.POST, request.FILES)

        if 'edit_product' in request.POST:
            product = Product.objects.filter(
                pk=request.POST['product_id']).first()
            product_update_form = UpdateProductForm(
                request.POST, request.FILES, instance=product)
            if product_update_form.is_valid():
                product_update_form.save()
                messages.success(request, 'The product has been updated')
                return redirect('/admins/dashboard/')
        else:
            product = Product.objects.filter(
                pk=request.POST['product_id']).first()
            product_update_form = UpdateProductForm(instance=product)

        if 'remove_product' in request.POST:
            product = Product.objects.filter(
                pk=request.POST['product_id']).first()
            product.delete()
            messages.success(
                request, f'The product {product} has been deleted')

        context['product_form'] = product_form
        context['product_update_form'] = product_update_form

    context['activatedashboard'] = 'active'
    context['products'] = products
    context['products_count'] = products_count
    context['user_count'] = user_count
    context['orders_count'] = orders_count

    return render(request, 'admins/dashboard.html', context)


def shipping(request):
    shipping = ShippingAddress.objects.all()
    if request.method == 'POST':
        if 'complete_shipping' in request.POST:
            current_shipping = ShippingAddress.objects.filter(
                pk=request.POST['shipping_id']).first()
            current_shipping.completed = True
            current_shipping.save()
        else:
            current_shipping = ShippingAddress.objects.filter(
                pk=request.POST['shipping_id']).first()

    context = {
        'activateorders': 'active',
        'shippings': shipping
    }
    return render(request, 'admins/orders.html', context)


def vieworder(request, pk):
    orders = OrderItem.objects.filter(order=pk)
    orderid = Order.objects.filter(pk=pk).first()
    context = {
        'activateorders': 'active',
        'orders': orders,
        'orderid': orderid
    }
    return render(request, 'admins/vieworder.html', context)


# def updatefileMF(request, file_id):
#     file = FileUpload.objects.get(id=file_id)
#     if request.method == "POST":
#         form = forms.FileForm(request.POST, request.FILES, instance=file)
#         if form.is_valid():
#             form.save()
#             return redirect('/products/getFileMF')

#     context = {
#         'form': forms.FileForm(instance=file),
#         'activate_fileMF': 'active'
#     }

#     return render(request, 'products/updateFileMF.html', context)
