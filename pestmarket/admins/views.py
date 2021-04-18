from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product, Order, OrderItem, ShippingAddress
from .forms import AddProductForm, UpdateProductForm

# Create your views here.


def dashboard(request):
    context = {}
    context['product_form'] = AddProductForm
    context['product_update_form'] = UpdateProductForm
    products = Product.objects.all()
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

    return render(request, 'admins/dashboard.html', context)


def shipping(request):
    shipping = ShippingAddress.objects.all()
    context = {
        'activateorders': 'active',
        'shippings': shipping
    }
    return render(request, 'admins/orders.html', context)


def vieworder(request, order_id):
    order = Order.objects.get(id=order_id)
    context = {
        'activateorders': 'active'
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
