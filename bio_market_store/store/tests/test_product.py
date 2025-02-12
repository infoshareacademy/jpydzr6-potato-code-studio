import datetime
from django.test import TestCase
from store.models import Product, UserProfile
from django.utils import timezone


class ProductTest(TestCase):
    def test_create_product(self):
        user_profile = UserProfile.objects.create_user(
            username="testuser", email="testuser@wp.pl", password="TestPassword123!"
        )

        product = Product.objects.create(
            user=user_profile,
            category='test',
            name_tag='test',
            price=10,
            commission=10,
            weight=10,
            exp_date=None,
            amount=10,
            producer="test",
            image="image.img",
        )

        self.assertEqual(product.category, 'test')
        self.assertEqual(product.name_tag, 'test')
        self.assertEqual(product.price, 10)
        self.assertEqual(product.commission, 10)
        self.assertEqual(product.weight, 10)
        self.assertEqual(product.amount, 10)
        self.assertEqual(product.producer, "test")
        self.assertEqual(product.image, "image.img")

        self.assertTrue(product.created_at >= timezone.now() - datetime.timedelta(seconds=1))
        self.assertTrue(product.created_at <= timezone.now())

        self.assertIsNone(product.exp_date)
