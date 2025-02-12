from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile, Product


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

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name_tag', 'price', 'commission', 'weight', 'exp_date', 'amount', 'producer',
                      'image']
