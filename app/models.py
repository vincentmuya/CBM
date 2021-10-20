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
class Computer(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField( null=True, blank=True)
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    stock = models.PositiveIntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    compcategory = models.ForeignKey('CompCategory', related_name="computers", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Computer, self).save(*args, **kwargs)

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