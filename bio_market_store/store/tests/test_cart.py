from django.test import TestCase, Client
from django.urls import reverse
from .models import Product, UserProfile
from django.contrib.auth.models import User

# How to RUN?
# python manage.py test store.tests.test_cart

class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.product = Product.objects.create(
            name_tag='Test Product',
            category='Supplements',
            price=29.99,
            commission=2.00,
            weight=0.5,
            amount=10,
            producer='Test Producer',
            image='test.png'
        )

    def test_add_to_cart(self):
        # Test adding new item to cart
        response = self.client.get(reverse('add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)

        session = self.client.session
        self.assertEqual(session['cart'][str(self.product.id)]['quantity'], 1)

        # Test adding existing item to cart
        response = self.client.get(reverse('add_to_cart', args=[self.product.id]))
        session = self.client.session
        self.assertEqual(session['cart'][str(self.product.id)]['quantity'], 2)

    def test_cart_counter(self):
        # Test cart counter with no items
        response = self.client.get(reverse('product_list'))
        self.assertContains(response, '<span class="...">0</span>', html=True)

        # Add item and test counter
        self.client.get(reverse('add_to_cart', args=[self.product.id]))
        response = self.client.get(reverse('product_list'))
        self.assertContains(response, '<span class="...">1</span>', html=True)

    def test_empty_cart(self):
        # Add item then empty cart
        self.client.get(reverse('add_to_cart', args=[self.product.id]))
        response = self.client.get(reverse('empty_cart'))
        self.assertRedirects(response, reverse('product_list'))

        session = self.client.session
        self.assertNotIn('cart', session)

    def test_cart_modal_content(self):
        # Test cart summary in modal
        self.client.get(reverse('add_to_cart', args=[self.product.id]))
        response = self.client.get(reverse('product_list'))

        self.assertContains(response, 'Test Product')
        self.assertContains(response, '29.99 zł')
        self.assertContains(response, 'Total: 29.99 zł')

    def test_payment_page(self):
        response = self.client.get(reverse('payment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment.html')

    def test_add_invalid_product(self):
        response = self.client.get(reverse('add_to_cart', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_cart_total_calculation(self):
        # Add 3 items and check total
        for _ in range(3):
            self.client.get(reverse('add_to_cart', args=[self.product.id]))

        response = self.client.get(reverse('product_list'))
        self.assertContains(response, 'Total: 89.97 zł')
        self.assertEqual(response.context['total_items'], 3)

    def test_cart_session_persistence(self):
        # Test cart persists across requests
        self.client.get(reverse('add_to_cart', args=[self.product.id]))
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.context['total_items'], 1)

        # New client session should have empty cart
        new_client = Client()
        response = new_client.get(reverse('product_list'))
        self.assertEqual(response.context['total_items'], 0)
