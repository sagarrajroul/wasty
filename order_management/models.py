from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    image_url = models.CharField(max_length=500, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.PositiveIntegerField()
    modified_on = models.DateTimeField(null=True)
    modified_by = models.PositiveIntegerField(null=True)

    objects = models.Manager()

    class Meta:
        ordering = ["name"]
        db_table = "PRODUCT"


class Wallet(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallet_user_history")
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.PositiveIntegerField()
    modified_on = models.DateTimeField(null=True)
    modified_by = models.PositiveIntegerField(null=True)

    objects = models.Manager()

    class Meta:
        db_table = "WALLET"


class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.PositiveIntegerField()
    modified_on = models.DateTimeField(null=True)
    modified_by = models.PositiveIntegerField(null=True)

    objects = models.Manager()

    class Meta:
        ordering = ["name"]
        db_table = "ITEM"


class WithdrawHistory(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="wallet_history")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_withdraw_history")
    amount_withdrawn = models.DecimalField(max_digits=10, decimal_places=2)
    withdrawn_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = "WITHDRAW_HISTORY"
