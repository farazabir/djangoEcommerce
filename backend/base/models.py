from itertools import product
from django.db import models
from user.models import CustomUser


class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True)
    brand = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True)
    description = models.TextField()
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stocks = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    rating = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.rating


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    taxprice = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True)
    totalPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.createdAt)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True)
    image = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postalCode = models.CharField(max_length=255)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True)

    def __str__(self):
        return self.address
