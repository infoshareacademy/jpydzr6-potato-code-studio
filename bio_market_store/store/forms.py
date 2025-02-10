from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile
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

class MiniQuizBioForm(forms.Form):
    answer = forms.ChoiceField(widget=forms.RadioSelect, choices=[], required=True)

    def __init__(self, *args, question=None, **kwargs):
        super().__init__(*args, **kwargs)
        if question:
            try:
                choices = json.loads(question.answer_choices) if isinstance(question.answer_choices, str) else question.answer_choices
                self.fields["answer"].choices = choices.items()
            except json.JSONDecodeError:
                self.fields["answer"].choices = []
