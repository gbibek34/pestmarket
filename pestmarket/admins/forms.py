from django.forms import ModelForm
from products.models import Product

# Create your forms here


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class UpdateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
