from django.contrib import admin

from .models import Bar, BarParticipant, BarTheme, Drink, Theme


class BarParticipantInline(admin.TabularInline):
    model = BarParticipant


class BarThemeInline(admin.TabularInline):
    model = BarTheme


class BarAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'degree', 'quantity', 'date_creation',
    )
    list_filter = (
        'theme', 'degree', 'quantity',
    )
    inlines = (BarParticipantInline, BarThemeInline,)


class DrinkAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)
    list_filter = ('degree',)


class ThemeAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)


admin.site.register(Bar, BarAdmin)
admin.site.register(Drink, DrinkAdmin)
admin.site.register(Theme, ThemeAdmin)
