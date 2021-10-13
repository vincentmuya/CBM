from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from slugify import slugify
from mptt.models import MPTTModel, TreeForeignKey

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


class Computer(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    stock = models.PositiveIntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    compcategory = models.ForeignKey(
        'CompCategory',
        related_name="computers",
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Computer, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return self.slug

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('comp_detail', args=[self.id, self.slug])

    @classmethod
    def search_by_name(cls, search_term):
        search_result = cls.objects.filter(name__icontains=search_term)
        return search_result


class CompCategory(MPTTModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name_plural = "compcategories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('computer_list_by_compcategory', args=[self.slug])