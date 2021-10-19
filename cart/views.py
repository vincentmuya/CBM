from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from app.models import Computer
from .cart import Cart
from .forms import CartAddProductForm, ShippingInformationForm
from django.contrib.auth.decorators import login_required
import random


@login_required(login_url='/accounts/login')
@require_POST
def cart_add(request, computer_id):
    cart = Cart(request)
    computer = get_object_or_404(Computer, id=computer_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(computer=computer,quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, computer_id):
    cart = Cart(request)
    computer = get_object_or_404(Computer, id=computer_id)
    cart.remove(computer)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    items = list(Computer.objects.all())
    random_items = random.sample(items, 4)
    random_items2 = random.sample(items, 4)
    random_items3 = random.sample(items, 4)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity':item['quantity'], 'update':True})
    return render(request, 'detail.html', {'cart': cart, 'random_items': random_items, 'random_items2': random_items2,
                                           'random_items3': random_items3})


def check_out(request):
    cart = Cart(request)
    return render(request, "checkOut.html")


def buyer_info(request):
    if request.method == 'POST':
        form = ShippingInformationForm(request.POST, request.FILES)
        if form.is_valid():
            buyer = form.save(commit=False)
            buyer.save()
            return HttpResponseRedirect('/')
    else:
        form = ShippingInformationForm()
    return render(request, 'buyer_form.html', {"form": form})
