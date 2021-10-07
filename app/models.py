from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from slugify import slugify

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, null=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])


class SubCategory(models.Model):
    parent_category = models.ForeignKey(Category, related_name='category', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True, null=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_subcategory', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='parent', null=True, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, related_name='child', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, null=True)
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (("id", "slug"),)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])

    @classmethod
    def search_by_name(cls,search_term):
        search_result = cls.objects.filter(name__icontains=search_term)
        return search_result
