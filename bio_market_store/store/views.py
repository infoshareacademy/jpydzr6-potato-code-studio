from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem


def index(request):
    global cart
    products = Product.objects.all()

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)

    context = {"products":products, "cart":cart}
    return render(request, "index.html", context)


def cart(request):

    cart = None
    cartitems = []

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitems = cart.cartitems.all()

    context = {"cart":cart, "items":cartitems}
    return render(request, "cart.html", context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get or initialize the cart in the session
    cart = request.session.get('cart', {})

    # Check if the product is already in the cart
    if str(product_id) in cart:
        # If the product is already in the cart, increase the quantity
        cart[str(product_id)]['quantity'] += 1
    else:
        # If the product is not in the cart, add it with a quantity of 1
        cart[str(product_id)] = {
            'name': product.name_tag,
            'price': str(product.price),  # Convert Decimal to string for session storage
            'quantity': 1,
        }

    # Save the updated cart back to the session
    request.session['cart'] = cart

    return redirect('cart_detail')  # Redirect to the cart detail page


def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []

    total_price = 0
    num_of_items = 0

    # Calculate total price and number of items
    for product_id, item in cart.items():
        product = {
            'id': product_id,
            'name': item['name'],
            'price': float(item['price']),  # Convert back to float for calculations
            'quantity': item['quantity'],
        }
        cart_items.append(product)

        total_price += product['price'] * product['quantity']
        num_of_items += product['quantity']

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'num_of_items': num_of_items,
    }

    return render(request, 'cart_detail.html', context)