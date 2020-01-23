import json

from django.db import models
import uuid


class InvoiceStatusConsts:
    NOTDONE = 'NOTDONE'
    DONE = 'DONE'

    states = (
        (NOTDONE, "NOTDONE"),
        (DONE, "DONE"),
    )


class City(models.Model):
    name = models.CharField(max_length=30)


class Address(models.Model):
    user = models.ForeignKey("snappfood.User", on_delete=models.PROTECT, null=True, related_name="address")
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    x = models.IntegerField()
    y = models.IntegerField()
    street = models.CharField(max_length=10)
    alley = models.CharField(max_length=10)
    plaque = models.CharField(max_length=10)


class Shop(models.Model):
    address = models.OneToOneField(Address, on_delete=models.PROTECT, related_name="shop")
    about_text = models.TextField()
    name = models.CharField(max_length=30)
    minimum_bill_value = models.IntegerField()


class Admin(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="admin")


class Category(models.Model):
    name = models.CharField(max_length=30)


class Food(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="food")
    price = models.IntegerField()
    name = models.CharField(max_length=100)
    about = models.TextField()
    discount = models.IntegerField()


class User(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    favorite = models.ManyToManyField(Food, related_name="liker")


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    items = models.ManyToManyField(Food, related_name="cart")


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")


class Discount(models.Model):
    users = models.ManyToManyField(User, related_name="discount")
    persent = models.IntegerField()


class Invoice(models.Model):
    items = models.ManyToManyField(Food, related_name="invoice")
    status = models.CharField(max_length=20, choices=InvoiceStatusConsts.states)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name="invoice")
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, blank=True, null=True, related_name="invoice")


class Comment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="comment")
    comment = models.IntegerField()
    text = models.TextField()
