from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import UserDrink, UserLanguage, UserTheme
from users.models import User


class UserDrinkInline(admin.TabularInline):
    model = UserDrink


class UserLanguageInline(admin.TabularInline):
    model = UserLanguage


class UserThemeInline(admin.TabularInline):
    model = UserTheme


class UserCustomAdmin(UserAdmin):
    inlines = (
        UserDrinkInline,
        UserLanguageInline,
        UserThemeInline
    )


admin.site.register(User, UserCustomAdmin)
