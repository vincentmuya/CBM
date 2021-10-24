from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from app.models import Computer
from app.forms import FeedbackInquiryForm
from .cart import Cart
from .forms import CartAddProductForm, ShippingInformationForm
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.conf import settings


@login_required(login_url='/accounts/login')
@require_POST
def cart_add(request, computer_id):
    cart = Cart(request)
    computer = get_object_or_404(Computer, id=computer_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(computer=computer, quantity=cd['quantity'], update_quantity=cd['update'])
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
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'detail.html', {'cart': cart, 'random_items': random_items, 'random_items2': random_items2,
                                           'random_items3': random_items3, 'feedback_form': feedback_form})


def check_out(request):
    cart = Cart(request)
    items = list(Computer.objects.all())
    random_items = random.sample(items, 4)
    random_items2 = random.sample(items, 4)
    random_items3 = random.sample(items, 4)
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, "checkOut.html", {'cart': cart, 'feedback_form': feedback_form, 'random_items': random_items,
                                             'random_items2': random_items2, 'random_items3': random_items3})


def buyer_info(request):
    items = list(Computer.objects.all())
    random_items = random.sample(items, 4)
    random_items2 = random.sample(items, 4)
    random_items3 = random.sample(items, 4)
    if request.method == 'POST':
        form = ShippingInformationForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            return HttpResponseRedirect('/cart/check_out')
    else:
        form = ShippingInformationForm()

    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = ":\n{}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)
            send_mail(subject, message, settings.SERVER_EMAIL, [sender])

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, 'buyer_form.html', {"form": form, 'feedback_form': feedback_form,
                                               'random_items': random_items, 'random_items2': random_items2,
                                               'random_items3': random_items3})
