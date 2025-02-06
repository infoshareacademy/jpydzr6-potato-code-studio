from django.contrib import messages
from store.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

@login_required
def add_product(request):
    if request.method == "POST":
        name_tag = request.POST.get("name_tag")
        category = request.POST.get("category")
        price = request.POST.get("price")
        commission = request.POST.get("commission")
        weight = request.POST.get("weight")
        exp_date = request.POST.get("exp_date")
        amount = request.POST.get("amount")
        producer = request.POST.get("producer")

        if not all([name_tag, category, price, commission, weight, exp_date, amount, producer]):
            return render(request, "add_product.html")

        product = Product(
            user=request.user,
            name_tag=name_tag,
            category=category,
            price=price,
            commission=commission,
            weight=weight,
            exp_date=exp_date,
            amount=amount,
            producer=producer,
            created_at=now(),
        )

        product.save()

        return redirect("/product_list")

    return render(request, "add_product.html")

def product_list(request):
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products})

def home_page(request):
    return render(request, "index.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        
        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")
        
        new_user = UserProfile.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        
        messages.success(request, "User created successfully")
        return redirect("home_page")

    return render(request, "register_page.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("home_page")

        
        return render(request, "login_page.html", {"error": "Invalid username or password"})
            
    return render(request, "login_page.html")

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout successful")
        return redirect("home_page")
    else:
        messages.error(request, "User is not authenticated")
        return redirect("home_page")