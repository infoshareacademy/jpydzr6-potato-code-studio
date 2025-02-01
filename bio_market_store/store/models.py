from django.db import models
from django.contrib.auth.models import AbstractUser
from store.utils.user_validator import UserValidator


class UserProfile(AbstractUser):
    user_validation = UserValidator()
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            "unique": "A user with that username already exists.",
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

class MiniQuizBio(models.Model):
    class AnswerChoices(models.TextChoices):
        A = 'a', 'A'
        B = 'b', 'B'
        C = 'c', 'C'
        D = 'd', 'D'

    question = models.TextField()
    answer_choices = models.JSONField()
    correct_answer = models.CharField(
        max_length=1,
        choices=AnswerChoices.choices
    )

    def __str__(self):
        return self.question
