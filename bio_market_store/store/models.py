from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Address(models.Model):
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="address",
    )

    def __str__(self):
        return f"{self.street}, {self.city}, {self.postal_code}, {self.phone_number}"
