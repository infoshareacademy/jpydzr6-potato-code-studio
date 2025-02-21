from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product


class CartTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass123')

        # Create a test product
        self.product = Product.objects.create(
            name_tag='Test Product',
            category='Test Category',
            price=10.00,
            commission=1.00,
            weight=0.5,
            amount=10,
            producer='Test Producer',
            image='test_image.png'
        )

        # Initialize the Django test client
        self.client = Client()

        # Log in the test user
        self.client.login(username='testuser', password='testpass123')

    def test_add_to_cart(self):
        """
        Test adding a product to the cart.
        """
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]))

        # Check that the product was added to the cart
        self.assertEqual(response.status_code, 302)  # Redirect after adding to cart
        self.assertIn(str(self.product.id), self.client.session['cart'])

    def test_increment_quantity(self):
        """
        Test incrementing the quantity of a product in the cart.
        """
        # Add the product to the cart first
        self.client.post(reverse('add_to_cart', args=[self.product.id]))

        # Increment the quantity
        response = self.client.get(reverse('increment_quantity', args=[self.product.id]))

        # Check that the quantity was incremented
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['quantity'], 2)  # Quantity should be 2 after incrementing

    def test_decrement_quantity(self):
        """
        Test decrementing the quantity of a product in the cart.
        """
        # Add the product to the cart first
        self.client.post(reverse('add_to_cart', args=[self.product.id]))

        # Increment the quantity to 2
        self.client.get(reverse('increment_quantity', args=[self.product.id]))

        # Decrement the quantity
        response = self.client.get(reverse('decrement_quantity', args=[self.product.id]))

        # Check that the quantity was decremented
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['quantity'], 1)  # Quantity should be 1 after decrementing

    def test_remove_product_from_cart(self):
        """
        Test removing a product from the cart by decrementing to zero.
        """
        # Add the product to the cart first
        self.client.post(reverse('add_to_cart', args=[self.product.id]))

        # Decrement the quantity to zero
        response = self.client.get(reverse('decrement_quantity', args=[self.product.id]))

        # Check that the product was removed from the cart
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['quantity'], 0)  # Quantity should be 0
        self.assertNotIn(str(self.product.id), self.client.session['cart'])  # Product should be removed from cart

    def test_add_to_cart_button_disabled(self):
        """
        Test that the "Add to Cart" button is disabled after adding a product to the cart.
        """
        # Add the product to the cart
        self.client.post(reverse('add_to_cart', args=[self.product.id]))

        # Load the product list page
        response = self.client.get(reverse('product_list'))

        # Check that the "Add to Cart" button is disabled
        self.assertContains(response, '<button class="btn btn-secondary btn-lg" disabled>Added to Cart</button>')

    def test_empty_cart(self):
        """
        Test emptying the cart.
        """
        # Add the product to the cart
        self.client.post(reverse('add_to_cart', args=[self.product.id]))

        # Empty the cart
        response = self.client.get(reverse('empty_cart'))

        # Check that the cart is empty
        self.assertEqual(response.status_code, 302)  # Redirect after emptying cart
        self.assertNotIn('cart', self.client.session)  # Cart should be empty
