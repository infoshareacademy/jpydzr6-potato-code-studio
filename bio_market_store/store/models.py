from django.db import models
from django.contrib.auth.models import AbstractUser

# from django.contrib.auth.models import User
from django.conf import settings
from .utils.user_validator import UserValidator
import json


class UserProfile(AbstractUser):
    base_roles = [("seller", "Seller"), ("client", "Client")]

    # user_validation = UserValidator()
    # username = models.CharField(
    #     max_length=150,
    #     unique=True,
    #     error_messages={
    #         "unique": "Username already exists",
    #     },
    # )
    # password = models.CharField(
    #     max_length=128,
    #     help_text=user_validation.get_help_text(),
    #     validators=[user_validation.validate],
    # )
    role = models.CharField(max_length=20, choices=base_roles, default="client")
    quiz_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.username}"

    @property
    def discount_voucher(self):
        return self.quiz_score // 25


class Address(models.Model):
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=9)
    state = models.CharField(max_length=50)
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="address",
    )

    def __str__(self):
        return f"{self.street}, {self.city}, {self.postal_code}, {self.phone_number}"


class AddressOptional(models.Model):
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=9)
    state = models.CharField(max_length=50)
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="address_optional",
    )

    def __str__(self):
        return f"{self.street}, {self.city}, {self.postal_code}, {self.phone_number}"


class Product(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products"
    )
    category = models.CharField(max_length=255)
    name_tag = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    commission = models.DecimalField(decimal_places=2, max_digits=10)
    weight = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    exp_date = models.DateField(null=True, blank=True)
    amount = models.IntegerField()
    producer = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="png")

    def __str__(self):
        return f"{self.name_tag} ({self.category})"


class MiniQuizBio(models.Model):
    question_text = models.TextField()
    answer_choices = models.TextField()
    correct_answer = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if isinstance(self.answer_choices, list):
            self.answer_choices = json.dumps(self.answer_choices)
        super().save(*args, **kwargs)

    def get_choices(self):
        if not self.answer_choices:
            return {}

        try:
            return json.loads(self.answer_choices)
        except json.JSONDecodeError:
            return {}

    def __str__(self):
        return self.question_text

class DiscountVoucher(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='vouchers')
    amount = models.PositiveIntegerField(default=1)  # zł
    created_at = models.DateTimeField(auto_now_add=True)
    is_redeemed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount} zł voucher for {self.user.username}"

