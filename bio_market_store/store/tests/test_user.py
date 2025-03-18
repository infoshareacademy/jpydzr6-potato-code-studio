from django.test import TestCase, Client
from django.urls import reverse
from store.models import UserProfile, Address
from store.forms import UserProfileForm, AddressForm


class UserProfileTest(TestCase):
    def test_create_user_profile_without_address(self):
        user_profile = UserProfile.objects.create_user(
            username="testuser",
            email="testuser@wp.pl",
            password="TestPassword123!",
            role="Seller",
        )
        self.assertEqual(user_profile.username, "testuser")
        self.assertEqual(user_profile.email, "testuser@wp.pl")
        self.assertEqual(user_profile.role, "Seller")
        self.assertFalse(hasattr(user_profile, "address"))
        self.assertTrue(user_profile.check_password, "TestPassword123!")

    def test_create_user_profile_with_address(self):
        user_profile = UserProfile.objects.create_user(
            username="testuser2",
            email="testuser2@wp.pl",
            password="TestPassword123!",
            role="Client",
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
        self.assertEqual(user_profile.role, "Client")
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


class UserAuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.user = UserProfile.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
            role="Client",
        )

    def test_register_user(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "newtestuser",
                "email": "newtestuser@example.com",
                "password": "TestPassword123!",
                "role": "Client",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_register_existing_user(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "testuser",
                "email": "anotheremail@example.com",
                "password": "TestPassword123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserProfile.objects.filter(username="testuser").exists())

    def test_login_valid_user(self):
        login = self.client.login(username="testuser", password="TestPassword123!")
        self.assertTrue(login)
        response = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "TestPassword123!",
            },
        )
        self.assertEqual(response.status_code, 200)
        user = UserProfile.objects.get(username="testuser")
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.id)

    def test_login_invalid_user(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "test_user3",
                "password": "TestPassword456!",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")

    def test_login_no_exist_user(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "noexistuser",
                "password": "SomePassword123!",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")


class UserProfileFormTest(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username="testuser",
            email="testuser@wp.pl",
            password="TestPassword123!",
            role="Client",
        )

    def test_user_profile_form_valid_data(self):
        form = UserProfileForm(
            data={
                "email": "newuser@wp.pl",
                "first_name": "John",
                "last_name": "Doe",
                "role": "client",
            }
        )
        self.assertTrue(form.is_valid())

    def test_user_profile_form_invalid_email(self):
        form = UserProfileForm(
            data={
                "email": "notanemail",
                "first_name": "John",
                "last_name": "Doe",
                "role": "client",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_update_user_profile(self):
        form = UserProfileForm(
            data={
                "email": "updateduser@wp.pl",
                "first_name": "Updated",
                "last_name": "User",
                "role": "client",
            },
            instance=self.user,
        )
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.user.refresh_from_db()
        self.assertEqual(updated_user.email, "updateduser@wp.pl")
        self.assertEqual(updated_user.first_name, "Updated")
        self.assertEqual(updated_user.last_name, "User")
