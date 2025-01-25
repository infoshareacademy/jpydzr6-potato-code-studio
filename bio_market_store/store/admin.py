from django.contrib import admin
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile, Address


# Register your models here.
class UserCreatingForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = ("username", "email", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput()


class UserPanelChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserProfile
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput()


class AddressInline(admin.StackedInline):
    model = Address
    can_delete = False


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name")
    add_form = UserCreatingForm
    change_form = UserPanelChangeForm
    inlines = (AddressInline,)
    fieldsets = [
        (None, {"fields": ("username", "password", "email")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email"),
            },
        ),
    ]


admin.site.register(UserProfile, UserProfileAdmin)
