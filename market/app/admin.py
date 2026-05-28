from django.contrib import admin
from .models import UserModel, ProductModel


admin.site.register(UserModel)

admin.site.register(ProductModel)