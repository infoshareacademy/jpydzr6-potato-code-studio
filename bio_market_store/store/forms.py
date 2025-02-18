from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import UserProfile, Product, Address, MiniQuizBio
import json


class UserCreatingForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget = forms.PasswordInput()
        self.fields["password2"].widget = forms.PasswordInput()


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254, widget=forms.TextInput(attrs={"autofocus": True})
    )
    password = forms.CharField(
        label="Password", strip=False, widget=forms.PasswordInput
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-conrol"}),
            "last_name": forms.TextInput(attrs={"class": "form-conrol"}),
            "email": forms.EmailInput(attrs={"class": "form-conrol"}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street", "postal_code", "city", "phone_number"]
        widgets = {
            "street": forms.TextInput(attrs={"class": "form-conrol"}),
            "postal_code": forms.TextInput(attrs={"class": "form-conrol"}),
            "city": forms.TextInput(attrs={"class": "form-conrol"}),
            "phone_number": forms.TextInput(
                attrs={"class": "form-conrol", "type": "tel", "pattern": "[0-9]{10}"}
            ),
        }


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
