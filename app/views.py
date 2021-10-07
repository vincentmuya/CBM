from django.shortcuts import render, get_object_or_404, redirect
from django.http  import HttpResponse
from .models import Product, Category, SubCategory
from django.http import JsonResponse, HttpResponseRedirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from cart.forms import CartAddProductForm
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
import requests

# Create your views here.


def getAccessToken(request):
    consumer_key = 'GjPRRmzBn870YZw2bqylAIlfAQE5aXa2'
    consumer_secret = 'yEb03uvft3dCrF7T'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)
def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254710902541,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254710902541,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Vincent",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')


def index(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    subcategory = SubCategory.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, "index.html", {'category': category, 'categories': categories, 'products': products, 'subcategory':subcategory})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    categories = Category.objects.all()
    cart_product_form = CartAddProductForm()
    return render(request, 'product_detail.html', {'product': product, 'categories': categories,
                                                   'cart_product_form': cart_product_form})


def on_sale(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, "on_sale.html", {'category': category, 'categories': categories, 'products': products})


def search_results(request):
    categories = Category.objects.all()
    if 'name' in request. GET and request.GET["name"]:
        search_term = request.GET.get("name")
        searched_ref = Product.search_by_name(search_term)
        message = f"{search_term}"
        return render(request, "search.html", {"message": message, "name": searched_ref, "categories": categories})
    else:
        message = "No match for search"
        return render(request, 'search.html')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "registration/register.html", {"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "registration/login.html", {"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")

