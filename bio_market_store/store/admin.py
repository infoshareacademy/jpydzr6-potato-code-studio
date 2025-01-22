from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


# Register your models here.
class UserProfileAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("address",)}),)


admin.site.register(UserProfile, UserProfileAdmin)
