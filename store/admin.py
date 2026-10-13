from django.contrib import admin
from .models import Category, Product, Order, OrderItem

### Allow viewing orders on order screen
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'price', 'quantity']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'amount_paid', 'date_ordered', 'status']
    readonly_fields = ['date_ordered']
    inlines = [OrderItemInline]

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)