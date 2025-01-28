import pytest
import uuid
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from store.models import Product, Cart, CartItem


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='12345')

@pytest.fixture
def product():
    return Product.objects.create(
        name="Test Product",
        price=10,
        loyalty_points=2,
        picture=SimpleUploadedFile("test.jpg", b"file_content")
    )

@pytest.fixture
def cart(user):
    return Cart.objects.create(user=user)

@pytest.fixture
def cart_item(cart, product):
    return CartItem.objects.create(product=product, cart=cart, quantity=2)

# Tests for the Product model
@pytest.mark.django_db
def test_product_creation(product):
    assert product.name == "Test Product"
    assert product.price == 10
    assert product.loyalty_points == 2
    assert product.picture.name == "img/test.jpg"
    assert str(product) == "Test Product"

# Tests for the Cart model
@pytest.mark.django_db
def test_cart_creation(cart, user):
    assert cart.user.username == 'testuser'
    assert cart.completed is False
    assert isinstance(cart.id, uuid.UUID)
    assert str(cart) == str(cart.id)

@pytest.mark.django_db
def test_cart_total_price(cart, product):
    CartItem.objects.create(product=product, cart=cart, quantity=2)
    assert cart.total_price == 20

@pytest.mark.django_db
def test_cart_num_of_items(cart, product):
    CartItem.objects.create(product=product, cart=cart, quantity=3)
    assert cart.num_of_items == 3

# Tests for the CartItem model
@pytest.mark.django_db
def test_cart_item_creation(cart_item, product, cart):
    assert cart_item.product.name == "Test Product"
    assert cart_item.cart.user.username == 'testuser'
    assert cart_item.quantity == 2
    assert str(cart_item) == "Test Product"

@pytest.mark.django_db
def test_cart_item_price(cart_item, product):
    assert cart_item.price == 20
