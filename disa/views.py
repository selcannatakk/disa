from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import *
from .cart import Cart


from django.http.response import JsonResponse


def index(request):
    categories = Category.objects.all()
    filter_id = request.GET.get('filter', 'all')

    if filter_id == 'all':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category__id=filter_id)

    context = {
        "products": products,
        "categories": categories,
    }


    return render(request, "index.html", context)


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        "product": product,

    }

    return render(request, "shop-detail.html", context)


def cart_summary(request):
    cart = Cart(request)

    products = cart.get_prods()
    prod_total_price = cart.prod_total_price()
    total_price = cart.total_price()
    quantities = request.session.get("cart")



    print(products)
    print(quantities)

    context = {
        "products": products,
        "quantities": quantities,
        "prod_total_price": prod_total_price,
        "total_price": total_price,

    }
    return render(request, "cart.html", context)


def add_to_cart(request):
    cart = Cart(request)

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        qty = int(request.POST.get("qty", 1))

        product = Product.objects.get(id=product_id)

        cart.add(product=product, qty=qty)
        cart_quantity = cart.__len__()

        print(request.session["cart"])
        print("cart number")

        context = {
            "cart_quantity": cart_quantity,
            "message": f"{product.name} Sepetinize eklendi.",

        }

        return JsonResponse(context)


def update_to_cart(request):
    cart = Cart(request)

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        btn_qty = request.POST.get("btn_qty")
        product = Product.objects.get(id=product_id)

        cart.update(product=product, btn_qty=btn_qty, qty=1)
        total_price = cart.total_price()

        for key, value in request.session.get("cart").items():
            if key == product_id:
                product_total_price = value["new_price"]

    context = {
        "product_total_price": product_total_price,
        "total_price":total_price,
        "message": "Sepetiniz güncellendi.",

    }

    return JsonResponse(context)


def delete_to_cart(request):
    
    cart = Cart(request)

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = Product.objects.get(id=product_id)
        cart.delete(product=product)
        cart_quantity = cart.__len__()
        total_price = cart.total_price()

    context = {
        "cart_quantity": cart_quantity,
        "total_price":total_price,
        "message": f"{product.name} Sepetinizden kaldırıldı.",

    }

    return JsonResponse(context)

def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.check_password(password):

                login(request, user)
                return redirect("index")

            else:
                messages.warning(request, "Paralonız Yanlış. Lütfen Tekrar Deneyiniz.")

        else:
            messages.warning(request, "E-Mail Adresiniz Yanlış. Lütfen Tekrar Deneyiniz.")

    return render(request, "login.html")


def user_register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not User.objects.filter(email=email).exits():
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            login(request, user)
            return redirect("index")

        else:
            messages.warning(request, "E-Mail Adresi Zaten Kullanılıyor. Lütfen Giriş Yapınız.")

    return render(request, "register.html")


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))
