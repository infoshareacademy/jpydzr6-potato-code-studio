from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    category = models.CharField(max_length=255)
    name_tag = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    commission = models.DecimalField(decimal_places=2, max_digits=10)
    weight = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    exp_date = models.DateField(null=True, blank=True)
    amount = models.IntegerField()
    producer = models.CharField(max_length=255)
    loyalty_points = models.IntegerField(default=0)
    image = models.ImageField(upload_to="png")

    def __str__(self):
        return f"{self.name_tag} ({self.category})"


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def total_price(self):
        cartitems = self.cartitems.all()
        total = sum([item.price for item in cartitems])
        return total

    @property
    def num_of_items(self):
        cartitems = self.cartitems.all()
        quantity = sum([item.quantity for item in cartitems])
        return quantity


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartitems")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name

    @property
    def price(self):
        new_price = self.product.price * self.quantity
        return new_price
