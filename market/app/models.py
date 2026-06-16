from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.contrib.postgres.fields import ArrayField
from decimal import Decimal
from payments import PurchasedItem
from payments.models import BasePayment
from typing import Iterable


import uuid


class Payment(BasePayment):
    def get_failure_url(self) -> str:
        return f"http://example.com/payments/{self.pk}/failure"
    
    def get_success_url(self):
        return f"http://example.com/payments/{self.pk}/success"
    
    def get_purchased_items(self) -> Iterable[PurchasedItem]:
        yield PurchasedItem()


class UserModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20, unique=True, validators=[MinLengthValidator(3)])
    email = models.EmailField(unique=True, validators=[MinLengthValidator(3)])
    password = models.CharField()
    avatar = models.ImageField(upload_to="avatars/")
    baskets = ArrayField(models.UUIDField(), editable=False, default=list)

    def delete(self, *args, **kwargs):
        if self.avatar:
            self.avatar.delete(save=False)
        super(UserModel, self).delete(*args, **kwargs)


class ProductModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    data = models.DateField(auto_now=True)
    price = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])
    text = models.TextField(max_length=400, validators=[MinLengthValidator(3)])
    img = models.ImageField(upload_to="products/")
    quantity = models.IntegerField(default=0)
    tags = ArrayField(models.CharField(max_length=20, validators=[MinLengthValidator(2)]), default=list)


    def delete(self, *args, **kwargs):
        if self.img:
            self.img.delete(save=False)
        super(ProductModel, self).delete(*args, **kwargs)