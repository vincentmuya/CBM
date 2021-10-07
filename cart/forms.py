from django import forms
from .models import BuyerInformation

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False,initial=False, widget=forms.HiddenInput)


class ShippingInformation(forms.Form):
    class Meta:
        model = BuyerInformation
        fields = ('buyer_name', 'buyer_number', 'buyer_location',)
        exclude = []
        widges = {
        }