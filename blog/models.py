from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.utils.text import slugify
from autoslug import AutoSlugField
from product.utils import make_thumbnail


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    body = models.TextField()
    slug = AutoSlugField(populate_from='title', unique_with='title')

    image = models.ImageField(upload_to='uploads/blogs/', blank=True)
    thumbnail = models.ImageField(upload_to='', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return f"/blog/{self.slug}/"

    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return f'https://tqt-rest-djshop.herokuapp.com{self.image.url}'
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return f'https://tqt-rest-djshop.herokuapp.com{self.thumbnail.url}'
        if self.image:
            size = (400, 300)
            self.thumbnail = make_thumbnail(self.image, size)
            self.save()
            return f'https://tqt-rest-djshop.herokuapp.com{self.thumbnail.url}'
        else:
            return ''

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_description(self):
        if len(self.description) > 20:
            return f'{self.description[:20]}...'
        else:
            return self.description

    def get_title(self):
        if len(self.title) > 40:
            return f'{self.title[:40]}...'
        else:
            return self.title
