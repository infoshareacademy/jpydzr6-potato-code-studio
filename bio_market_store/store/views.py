from django.shortcuts import render, redirect
from .models import Product
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

@login_required
def add_product(request):
    if request.method == "POST":
        # Pobranie danych z formularza
        name_tag = request.POST.get("name_tag")
        category = request.POST.get("category")
        price = request.POST.get("price")
        commission = request.POST.get("commission")
        weight = request.POST.get("weight")
        exp_date = request.POST.get("exp_date")
        amount = request.POST.get("amount")
        producer = request.POST.get("producer")

        if not all([name_tag, category, price, commission, weight, exp_date, amount, producer]):
            return HttpResponse("Błąd: Wszystkie pola są wymagane!")

        product = Product(
            user=request.user,
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

        return redirect("/products")

    return render(request, "add_product.html")

def product_list(request):
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products})

# Create your views here.