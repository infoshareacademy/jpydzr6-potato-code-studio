from django.test import TestCase
from store.models import UserProfile, Address


class UserProfileTest(TestCase):
    def test_create_user_profile_without_address(self):
        user_profile = UserProfile.objects.create_user(
            username="testuser", email="testuser@wp.pl", password="TestPassword123!"
        )
        self.assertEqual(user_profile.username, "testuser")
        self.assertEqual(user_profile.email, "testuser@wp.pl")
        self.assertFalse(hasattr(user_profile, "address"))
        self.assertTrue(user_profile.check_password, "TestPassword123!")

    def test_create_user_profile_with_address(self):
        user_profile = UserProfile.objects.create_user(
            username="testuser2",
            email="testuser2@wp.pl",
            password="TestPassword123!",
        )
        user_address = Address.objects.create(
            street="123 Test St",
            postal_code="12345",
            city="Test City",
            phone_number="1234567890",
            user=user_profile,
        )

        # Assertions to test user_profile
        self.assertEqual(user_profile.username, "testuser2")
        self.assertEqual(user_profile.email, "testuser2@wp.pl")
        self.assertEqual(user_profile.address.street, "123 Test St")
        self.assertEqual(user_profile.address.postal_code, "12345")
        self.assertEqual(user_profile.address.city, "Test City")
        self.assertEqual(user_profile.address.phone_number, "1234567890")
        self.assertTrue(user_profile.check_password, "TestPassword123!")

        # Assertions to test user_address
        self.assertEqual(user_address.street, "123 Test St")
        self.assertEqual(user_address.postal_code, "12345")
        self.assertEqual(user_address.city, "Test City")
        self.assertEqual(user_address.phone_number, "1234567890")
        self.assertEqual(user_address.user, user_profile)
