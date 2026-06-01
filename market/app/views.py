from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import UserModel, ProductModel
from .forms import UserForm, AuthForm


import bcrypt


def main(request):
    status = False
    if "username" in request.session:
        products = ProductModel.objects.all()
        user = request.session["username"]
        status = True
        return render(request, "main.html", {"products": products, "user": user, "status": status})
    return render(request, "main.html", {"status": status })


def goods(request):
    return render(request, "goods.html")


def basket(request):
    return render(request, "basket.html")


def company(request):
    return render(request, "company.html")


def user(request):
    userform = UserForm(request.POST, request.FILES)
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        avatar = request.POST.get("avatar")
        password_str = str(password)
        password_hash = bcrypt.hashpw(password_str.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = UserModel(username=username, email=email, password=password_hash, avatar=avatar)
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
            password = str(username.password).encode("utf-8")
            hash_password = bcrypt.checkpw(password_encode, password)
            if hash_password:
                request.session["username"] = username.username
                return redirect("/main")
            else:
                return HttpResponse("<h1>Неправильный пароль</h1>")
        except ObjectDoesNotExist:
            return HttpResponse("<h1>Такого пользователя нет</h1>")
    return render(request, "auth.html", {"form": authform})


def profile(request):
    if "username" in request.session:
        user = request.session["username"]
        profile = UserModel.objects.get(username=user)
        return render(request, "profile.html", {"user": user, "profile": profile})
    else:
        return redirect("/auth")
    

def exit_profile(request):
    if "username" in request.session:
        try:
            del request.session["username"]
        except KeyError:
            return HttpResponse(f"{KeyError}", status=400)
        return redirect("/main")
    return redirect("/main")
    

def delete_profile(request):
    if "username" in request.session:
        user = request.session["username"]
        user_model = UserModel.objects.get(username=user)
        user_model.delete_user()
        return redirect("/main")
    return redirect("/main")