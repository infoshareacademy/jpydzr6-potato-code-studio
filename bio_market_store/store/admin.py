from django.contrib import admin
from django import forms
from django.contrib.auth.forms import UserChangeForm, AdminPasswordChangeForm
from .models import UserProfile, Address
from .forms import UserCreatingForm


# Register your models here.
class UserPanelChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserProfile
        fields = (
            "username",
            "email",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["password"].widget = forms.PasswordInput()


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

    change_password_form = AdminPasswordChangeForm

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)


admin.site.register(UserProfile, UserProfileAdmin)
