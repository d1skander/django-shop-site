from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import UserModel, ProductModel
from .forms import UserForm, AuthForm


import bcrypt


def main(request):
    if "username" in request.session:
        products = ProductModel.objects.all()
        user = request.session["username"]
        return render(request, "main.html", {"products": products, "user": user})
    return redirect("/user")


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
    authform = AuthForm()
    if request.method == "POST":
        username_request = request.POST.get("username")
        password_request = request.POST.get("password")
        password_encode = str(password_request).encode("utf-8")
        try:
            username = UserModel.objects.get(username=username_request)
            password = username.password
            hash_password = bcrypt.checkpw(password_encode, password.encode("utf-8"))
            if hash_password:
                request.session["username"] = username.username
                return redirect("/main")
            else:
                return HttpResponse("<h1>Неправильный пароль</h1>")
        except ObjectDoesNotExist:
            return HttpResponse("<h1>Такого пользователя нет</h1>")
    return render(request, "auth.html", {"form": authform})