from django.contrib import admin
from .models import Category, Product, SubCategory, Computer, CompCategory

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Computer)
admin.site.register(CompCategory)
