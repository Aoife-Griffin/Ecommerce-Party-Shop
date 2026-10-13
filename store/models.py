from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name
    ### Stops admin from showing categories
    class Meta:
        verbose_name_plural = 'categories'

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')

    # Add Sale Attributes
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    ### Adding in stock validation
    stock = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.name



class Order(models.Model):
    ### Changed for multi orders in the checkout
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250, default="")
    email = models.EmailField(max_length=250, default="")
    shipping_address = models.TextField(max_length=1500, default="")
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    date_ordered = models.DateTimeField(auto_now_add=True)

    ### Safeguard added for validation
    status = models.CharField(max_length=50, default='Demo - Not Paid')
    
    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


### Seperate orderitem for point-of-checkout snapshot logs
class OrderItem(models.Model):
    ### Links order to inventory table
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    ### Hardcodes product info so receipts won't change if the price/qty/name changes after buying it
    product_name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product_name} ({self.quantity})"