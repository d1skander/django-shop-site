from django.shortcuts import render, redirect
from .models import UserModel, ProductModel
from .forms import UserForm


import bcrypt


def main(request):
    products = ProductModel.objects.all()
    return render(request, "main.html", {"products": products})


def goods(request):
    return render(request, "goods.html")


def basket(request):
    return render(request, "basket.html")


def company(request):
    return render(request, "company.html")


def user(request):
    userform = UserForm()
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_hash = bcrypt.hashpw(str(password).encode("utf-8"), bcrypt.gensalt())
        user = UserModel(username=username, email=email, password=password_hash)
        user.save()
        return redirect("/main")
    return render(request, "user.html", {"form": userform})


def auth(request):
    return render(request, "auth.html")