from django.contrib import messages
from store.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now


def cover_page(request):
    return render(request, 'cover.html')


def about_us(request):
    return render(request, 'about.html')


def contact_us(request):
    return render(request, 'contact.html')


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
        image = request.FILES.get("image")

        if not all([name_tag, category, price, commission, weight, exp_date, amount, producer, image]):
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
            image=image,
            created_at=now(),
        )
        product.save()
        return redirect("/product_list")

    return render(request, "add_product.html")


def product_list(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {})

    total_items = 0
    cart_total = 0.0

    # Calculate total items and cart total
    for item in cart.values():
        total_items += item['quantity']
        cart_total += float(item['price']) * item['quantity']

    return render(request, "product_list.html", {
        "products": products,
        "cart_total": cart_total,
        "total_items": total_items
    })


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
    else:
        messages.error(request, "User is not authenticated")
    return redirect("home_page")


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    product_key = str(product_id)

    if product_key in cart:
        cart[product_key]['quantity'] += 1
    else:
        cart[product_key] = {
            'quantity': 1,
            'price': str(product.price),
            'name': product.name_tag,
            'image': product.image.url
        }

    request.session['cart'] = cart
    request.session.modified = True  # Critical fix
    return redirect('product_list')


def empty_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('product_list')


def payment(request):
    return render(request, 'payment.html')
