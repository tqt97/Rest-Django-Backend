from django.contrib import admin
from .models import *
# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user','email', 'created_at']
    list_filter = ['user','created_at']
    search_fields = ['first_name','last_name','email','address','zipcode','place','phone']
    inlines = [OrderItemInline]
    
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
