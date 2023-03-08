from django.contrib import admin

from .models import Bar, BarParticipant, Drink, Language, Theme


class BarParticipantInline(admin.TabularInline):
    model = BarParticipant


class BarAdmin(admin.ModelAdmin):
    list_display = (
        'theme', 'language', 'degree', 'quantity', 'date_creation',
    )
    list_filter = (
        'theme', 'language', 'degree', 'quantity',
    )
    inlines = (BarParticipantInline,)


class DrinkAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)
    list_filter = ('degree',)


class LanguageAdmin(admin.ModelAdmin):
    search_fields = ('name', 'abbreviation')
    list_display = ('name',)


class ThemeAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)


admin.site.register(Bar, BarAdmin)
admin.site.register(Drink, DrinkAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Theme, ThemeAdmin)
