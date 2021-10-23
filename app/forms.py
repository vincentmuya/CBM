from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.
APPLICATION_USE = [
    ("", ""),
    ('government', 'Government'),
    ('commercial', 'Commercial'),
    ('non_profit', 'Non-Profit'),
    ]


PRODUCT_TO_SELECT = [
    ("", ""),
    ('iridesse', 'Xerox Iridesse'),
    ('versant_4100', 'Xerox Versant 4100 Press'),
    ('primelink_b9100', 'Xerox Primelink B9100 Series'),
    ]


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class QuoteForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField(required=True)
    phone_number = forms.IntegerField()
    product = forms.CharField(required=True, label='Select product you want to get the quote for', widget=forms.Select(choices=PRODUCT_TO_SELECT))
    application = forms.CharField(required=True, label='Select application of product', widget=forms.Select
    (choices=APPLICATION_USE))
