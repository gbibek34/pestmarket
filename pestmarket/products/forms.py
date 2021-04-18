from django.forms import ModelForm
from .models import ShippingAddress


class CheckoutForm(ModelForm):
    class Meta:
        exclude = ('customer', 'order', 'completed')
        model = ShippingAddress

    def save(self, user, order):
        shipping_address = ShippingAddress.objects.create(
            customer=user,
            order=order,
            contactno=self.cleaned_data['contactno']
        )
        return shipping_address
