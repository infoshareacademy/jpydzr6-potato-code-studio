from django.test import TestCase

# store/tests.py
from django.test import TestCase
from django.urls import reverse
from .models import Product, Cart


class StoreTests(TestCase):
    def setUp(self):
        # Create test product
        self.product = Product.objects.create(
            category='Fruits',
            name='Test Apples',
            price=3.00,
            commission=3,
            weight=10,
            exp_date='2025-04-04',
            producer='Test Farm'
        )

    def test_product_creation(self):
        """Test product model creation"""
        self.assertEqual(self.product.name, 'Test Apples')
        self.assertEqual(self.product.category, 'Fruits')
        self.assertEqual(str(self.product), 'Test Apples')

    def test_cart_creation(self):
        """Test cart model creation and relationships"""
        cart_item = Cart.objects.create(product=self.product, quantity=2)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(str(cart_item), 'Test Apples - 2')

    def test_product_list_view(self):
        """Test product listing page"""
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_list.html')
        self.assertContains(response, 'Test Apples')

    def test_update_cart_view_increment(self):
        """Test adding items to cart"""
        response = self.client.get(reverse('update_cart', args=[self.product.id, 1]))
        self.assertEqual(response.status_code, 302)  # Check redirect
        cart_item = Cart.objects.get(product=self.product)
        self.assertEqual(cart_item.quantity, 1)

    def test_update_cart_view_decrement(self):
        """Test removing items from cart"""
        # First add some items
        Cart.objects.create(product=self.product, quantity=3)

        response = self.client.get(reverse('update_cart', args=[self.product.id, -1]))
        cart_item = Cart.objects.get(product=self.product)
        self.assertEqual(cart_item.quantity, 2)

    def test_update_cart_negative_quantity(self):
        """Test quantity doesn't go below zero"""
        response = self.client.get(reverse('update_cart', args=[self.product.id, -1]))
        cart_item = Cart.objects.get(product=self.product)
        self.assertEqual(cart_item.quantity, 0)

    def test_empty_cart_view(self):
        """Test cart emptying functionality"""
        # Add items to cart
        Cart.objects.create(product=self.product, quantity=2)

        response = self.client.get(reverse('empty_cart'))
        self.assertEqual(Cart.objects.count(), 0)
        self.assertEqual(response.status_code, 302)  # Check redirect

    def test_order_summary_view(self):
        """Test order summary page"""
        # Add items to cart
        Cart.objects.create(product=self.product, quantity=2)

        response = self.client.get(reverse('order_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/order_summary.html')
        self.assertContains(response, 'Test Apples')
        self.assertContains(response, '6.00')  # 2 items * 3.00 PLN

    def test_url_resolution(self):
        """Test URL patterns resolve correctly"""
        url = reverse('update_cart', args=[1, 1])
        self.assertEqual(url, '/update_cart/1/1/')

        url = reverse('order_summary')
        self.assertEqual(url, '/order_summary/')

