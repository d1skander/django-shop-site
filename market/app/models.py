from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator


class UserModel(models.Model):
    id = models.IntegerField(default=None, primary_key=True)
    username = models.CharField(max_length=20, unique=True, validators=[MinLengthValidator(3)])
    email = models.EmailField(unique=True, validators=[MinLengthValidator(3)])
    password = models.CharField(max_length=20)


class ProductModel(models.Model):
    id = models.IntegerField(default=None, primary_key=True)
    data = models.DateField(auto_now=True)
    price = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])
    text = models.TextField(max_length=400, validators=[MinLengthValidator(3)])


    def __str__(self):
        return str(self.data)