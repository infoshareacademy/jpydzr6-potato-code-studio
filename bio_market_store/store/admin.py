from django.contrib import admin

from .models import UserProfile


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name")


admin.site.register(UserProfile, UserProfileAdmin)
