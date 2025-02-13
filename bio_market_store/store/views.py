from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart


def product_list(request):
    products = Product.objects.all()

    # Get cart quantities for each product
    for product in products:
        cart_item = Cart.objects.filter(product=product).first()
        product.cart_quantity = cart_item.quantity if cart_item else 0

    return render(request, 'store/product_list.html', {'products': products})


def update_cart(request, product_id, change):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(product=product)

    # Convert 'change' to an integer
    change = int(change)

    cart_item.quantity += change
    if cart_item.quantity < 0:
        cart_item.quantity = 0
    cart_item.save()

    # Return the updated quantity and total price as JSON
    return JsonResponse({
        'quantity': cart_item.quantity,
        'total_price': calculate_total_price(),  # You need to implement this function
    })

def calculate_total_price():
    cart_items = Cart.objects.filter(quantity__gt=0)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return total_price

def order_summary(request):
    cart_items = Cart.objects.filter(quantity__gt=0)

    # Calculate the total price for each item and add it to the context
    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    # Calculate the overall total price
    total_price = sum(item.total_price for item in cart_items)

    return render(request, 'store/order_summary.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def empty_cart(request):
    Cart.objects.all().delete()  # Empty the cart
    return redirect('product_list')  # Redirect to the main page