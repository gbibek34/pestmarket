from django.forms import ModelForm
from .models import ShippingAddress


class CheckoutForm(ModelForm):
    class Meta:
        exclude = ('customer', 'order')
        model = ShippingAddress

    def save(self, user, order):
        shipping_address = ShippingAddress.objects.create(
            customer=user,
            order=order,
            address=self.cleaned_data['address'],
            contactno=self.cleaned_data['contactno']
        )
        return shipping_address
