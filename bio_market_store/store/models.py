from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    user_id = models.ForeignKey(
        "UserProfile", on_delete=models.CASCADE, related_name="address_user", null=True
    )

    def __str__(self):
        return f"{self.street}, {self.city}"


class UserProfile(AbstractUser):
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="customer_profile",
    )

    def __str__(self):
        return f"{self.username}"
