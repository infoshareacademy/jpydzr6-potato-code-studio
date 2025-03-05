from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User
from django.conf import settings
from .utils.user_validator import UserValidator
import json


class UserProfile(AbstractUser):
    user_validation = UserValidator()
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            "unique": "Username already exists",
        },
    )
    password = models.CharField(
        max_length=128,
        help_text=user_validation.get_help_text(),
        validators=[user_validation.validate],
    )

    def __str__(self):
        return f"{self.username}"


class Address(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField(max_length=50, blank=True, help_text="e.g., Home, Office")
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Poland')
    state = models.CharField(max_length=100, default='mazowieckie')
    phone_number = models.CharField(max_length=10)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Get existing count before saving
        if not self.pk:  # Only for new instances
            count = Address.objects.filter(user=self.user).count()
            self.name = f"Address {count + 1}"
        super().save(*args, **kwargs)

    def clean(self):
        if not self.pk and self.user.addresses.count() >= 2:
            raise ValidationError("User cannot have more than two addresses.")

    def __str__(self):
        return f"{self.name}: {self.street}, {self.city}"


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
