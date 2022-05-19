from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class Shop(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=255)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE, default = 1)
    description = models.TextField(blank=True)
    imageUrl = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.name



class Cart(models.Model):
    user = models.OneToOneField(
        User, related_name="user_cart", on_delete=models.CASCADE, primary_key=True
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True, null=True
    )

@receiver(post_save, sender=User)
def create_user_cart(sender, created, instance, *args, **kwargs):
    if created:
        Cart.objects.create(user=instance)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_item", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="cart_product", on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)