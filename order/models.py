from django.contrib.auth.models import User
from django.db import models
from django.contrib.humanize.templatetags import humanize
from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        User, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    zipcode = models.CharField(max_length=20)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    stripe_token = models.CharField(max_length=100)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Order ID: {self.id} - by  <{self.user}>'
    
    def get_date(self):
        return humanize.naturaltime(self.created_at)

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    def get_date(self):
        return humanize.naturaltime(self.created_at)
