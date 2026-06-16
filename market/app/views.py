from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template.response import TemplateResponse
from .models import UserModel, ProductModel
from .forms import UserForm, AuthForm
from payments import get_payment_model, RedirectNeeded


import bcrypt
import uuid


def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(request, 'payment.html', {"form": form, "payment": payment})


def main(request):
    status = False
    if "username" in request.session:
        products = ProductModel.objects.all()
        user = request.session["username"]
        status = True
        return render(request, "main.html", {"products": products, "user": user, "status": status})
    return render(request, "main.html", {"status": status })


def goods(request):
    if "username" in request.session:
        cookie = request.COOKIES["tags"]
        tags = [i for i in str(cookie).replace("[", "").replace("]", "").split(',')]
        products = []
        for product in ProductModel.objects.all().iterator():
            for tag in tags:
                print(tag.encode("utf-8").decode("utf-8"), tag.encode("utf-8"), product.tags, tag.encode("utf-8").decode("utf-8") in product.tags)
                if tag.encode("utf-8").decode("utf-8") in product.tags:
                    products.append(product.id)
                else:
                    return render(request, "goods.html")
        for id_p in products:
            object = ProductModel.objects.all().filter(id=id_p)
            return render(request, "goods.html", {"products": object})
        return render(request, "goods.html")
    return render(request, "goods.html")


def basket(request):
    if "username" in request.session:
        session = request.session["username"]
        user = UserModel.objects.get(username=session)
        baskets = user.baskets
        for basket in baskets:
            products = ProductModel.objects.all().filter(id=basket)
            return render(request, "basket.html", {"products": products})
    return render(request, "basket.html")


def basket_goods(request):
    if request.method == "POST":
        id_basket = request.POST.get("id_basket")
        if "username" in request.session:
            session = request.session["username"]
            user = UserModel.objects.get(username=session)
            user.baskets.append(id_basket)
            user.save()
            return HttpResponse(status=204)
        return HttpResponse(status=400)
    else:
        return HttpResponse(status=409)
    

def basket_delete(request):
    if request.method == "POST":
        r_id_basket = request.POST.get("id_basket")
        id_basket = uuid.UUID(r_id_basket)
        if "username" in request.session:
            session = request.session["username"]
            user = UserModel.objects.get(username=session)
            try:
                user.baskets.remove(id_basket)
                user.save()
                return HttpResponse(status=204)
            except ValueError:
                return HttpResponse(status=302)
        return HttpResponse(status=400)
    else:
        return HttpResponse(status=409)
    

def tags_cookie(request):
    if "username" in request.session:
        if request.method == "POST":
            tags = request.POST.get("tags")
            str_tags = str(tags).replace("{", "").replace("}", "")
            split_tags = str_tags.strip().split(",")
            byte_tags = [i.encode('utf-8') for i in split_tags]
            resp = HttpResponse()
            resp.set_cookie("tags", byte_tags)
            return resp
        return redirect("/main")
    return redirect("/main")


def company(request):
    return render(request, "company.html")


def user(request):
    userform = UserForm(request.POST, request.FILES)
    if request.method == "POST":
        userform = UserForm(request.POST, request.FILES)
        if userform.is_valid():
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            avatar = userform.cleaned_data.get("avatar")
            password_str = str(password)
            password_hash = bcrypt.hashpw(password_str.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            user = UserModel(username=username, email=email, password=password_hash, avatar=avatar)
            user.save()
            return redirect("/main")
        return render(request, "user.html", {"form": userform})
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
        try:
            profile = UserModel.objects.get(username=user)
            return render(request, "profile.html", {"user": user, "profile": profile})
        except ObjectDoesNotExist:
            return redirect("/auth")
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
        try:
            del request.session["username"]
        except KeyError:
            return HttpResponse(f"{KeyError}", status=400)
        user_model.delete()
        return redirect("/main")
    return redirect("/main")