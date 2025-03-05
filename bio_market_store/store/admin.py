from django.contrib import admin
from django import forms
from django.contrib.auth.forms import UserChangeForm, AdminPasswordChangeForm
from .models import UserProfile, Address, MiniQuizBio, Product  # Import the Product model
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
    extra = 0
    max_num = 2



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


# Register the Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_tag', 'category', 'price', 'amount', 'producer', 'created_at')  # Fields to display in the list view
    list_filter = ('category', 'created_at')  # Filters for the right sidebar
    search_fields = ('name_tag', 'producer')  # Search bar fields
    ordering = ('-created_at',)  # Default ordering (newest first)


# Register other models
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(MiniQuizBio)
