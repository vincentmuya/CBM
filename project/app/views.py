from django.shortcuts import render, get_object_or_404, redirect
from django.http  import HttpResponse
from .models import Product, Category
from django.http import JsonResponse, HttpResponseRedirect
# Create your views here.


def index(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()[:4]
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, "index.html", {'category': category,'categories': categories, 'products': products})
