from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from django.contrib.auth import get_user_model
from .models import UserProfile, Product, Address, MiniQuizBio, AddressOptional
from .utils.user_registration import ROLE_CHOICES
import json
from django.conf import settings


class UserCreatingForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = ("username", "email", "password1", "password2", "role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if settings.DEBUG:
            self.fields["role"].choices.append(("contributor", "Contributor"))

        self.fields["username"].widget = forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter username"}
        )
        self.fields["email"].widget = forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter email"}
        )
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter password",
                "id": "password",
            }
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm password",
                "id": "confirm_password",
            }
        )
        self.fields["role"].widget = forms.Select(
            attrs={"class": "form-control", "placeholder": "Select role"},
            choices=ROLE_CHOICES,
        )


class UserAuthenticationForm(AuthenticationForm):
    class Meta:
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": f"Enter {field.label.lower()}",
                }
            )

        self.fields["username"].widget.attrs["autofocus"] = True


class UserProfileForm(forms.ModelForm):
    base_roles = [("seller", "Seller"), ("client", "Client")]

    if settings.DEBUG:
        base_roles.append(("contributor", "Contributor"))

    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "email", "role"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your first name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your last name",
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter your email"}
            ),
            "role": forms.Select(
                attrs={"class": "form-control", "placeholder": "Select your role"}
            ),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street", "postal_code", "city", "phone_number", "state"]
        widgets = {
            "street": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter street name"}
            ),
            "postal_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter postal code"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter city"}
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "type": "tel",
                    "pattern": "[0-9]{9}",
                    "placeholder": "Enter phone number",
                }
            ),
            "state": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        # Dynamically set the model based on the instance passed to the form
        if 'instance' in kwargs and isinstance(kwargs['instance'], AddressOptional):
            self.Meta.model = AddressOptional  # Switch to AddressOptional model
        super().__init__(*args, **kwargs)


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.PasswordInput(
            attrs={"class": "form-control"}
        )
        self.fields["new_password1"].widget = forms.PasswordInput(
            attrs={"class": "form-control"}
        )
        self.fields["new_password2"].widget = forms.PasswordInput(
            attrs={"class": "form-control"}
        )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "name_tag",
            "price",
            "commission",
            "weight",
            "exp_date",
            "amount",
            "producer",
            "description",
            "image",
        ]


class MiniQuizBioForm(forms.Form):
    answer = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[],
        required=True,
    )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop("question", None)
        super().__init__(*args, **kwargs)

        if question:
            if isinstance(question.answer_choices, str):
                answer_choices = json.loads(question.answer_choices)
            else:
                answer_choices = question.answer_choices

            self.fields["answer"].choices = [
                (key, value) for key, value in answer_choices.items()
            ]
