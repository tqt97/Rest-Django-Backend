from django.db import models
from django.utils.text import slugify
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize
from .utils import make_thumbnail


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique_with='name')

    class Meta:
        verbose_name = 'Categories'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique_with='name')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(
        upload_to='uploads/products/', blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return f'https://tqt-rest-djshop.herokuapp.com{self.image.url}'
        else:
            return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return f'https://tqt-rest-djshop.herokuapp.com{self.thumbnail.url}'
        if self.image:
            size = (300, 300)
            self.thumbnail = make_thumbnail(self.image, size)
            self.save()
            return f'https://tqt-rest-djshop.herokuapp.com{self.thumbnail.url}'
        else:
            return ''

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_rating(self):
        reviews_total = sum(review.rating for review in self.reviews.all())

        if reviews_total > 0:
            return round(int(reviews_total / self.reviews.count()))

        return 0

    def get_name(self):
        if len(self.name) > 40:
            return f'{self.name[:40]}...'
        else:
            return self.name

class Review(models.Model):
    product = models.ForeignKey(
        Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)
    content = models.TextField()
    created_by = models.ForeignKey(
        User, related_name='reviews', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} - {self.rating}'

    def get_product(self):
        return self.product.name

    def get_user(self):
        return self.created_by.username

    def get_date(self):
        return humanize.naturaltime(self.created_at)
