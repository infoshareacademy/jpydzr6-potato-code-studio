from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from django.contrib.auth import get_user_model
from .models import UserProfile, Product, Address, MiniQuizBio
import json

# Voivodeship choices for address forms
VOIVODESHIPS = [
    ('', 'Choose...'),
    ('Lower Silesia', 'Lower Silesia'),
    ('Kuyavia-Pomerania', 'Kuyavia-Pomerania'),
    ('Lodzkie', 'Lodzkie'),
    ('Lublin', 'Lublin'),
    ('Lubusz', 'Lubusz'),
    ('Lesser Poland', 'Lesser Poland'),
    ('Masovia', 'Masovia'),
    ('Subcarpathian', 'Subcarpathian'),
    ('Pomerania', 'Pomerania'),
    ('West Pomerania', 'West Pomerania'),
    ('Greater Poland', 'Greater Poland'),
    ('Podlaskie', 'Podlaskie'),
    ('Świętokrzyskie', 'Świętokrzyskie'),
    ('Opolskie', 'Opolskie'),
]

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
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

class AddressForm(forms.ModelForm):
    state = forms.ChoiceField(
        choices=VOIVODESHIPS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Voivodeship"
    )

    class Meta:
        model = Address
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Home, Office, etc.'
            }),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'tel',
                    'pattern': '[0-9]{9}',
                    'placeholder': '123456789'
                }
            ),
            'address2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional'
            }),
        }
        labels = {
            'address2': 'Address Line 2 (Optional)'
        }

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

# Updated formset using the custom AddressForm
AddressFormSet = inlineformset_factory(
    UserProfile,
    Address,
    form=AddressForm,
    extra=1,
    max_num=2,
    can_delete=True
)
