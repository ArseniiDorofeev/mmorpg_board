from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ckeditor.widgets import CKEditorWidget
from django.db import models
from .models import CustomUser, UserProfile, Advertisement


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_verified')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_verified',)}),
    )


class UserProfileAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }


class AdvertisementAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)
