from django.contrib import admin
from .models import Profile, MajorOption, CountryOption


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'degree_level', 'major', 'country', 'target_country', 'gpa')
    list_filter = ('degree_level', 'country', 'target_country')
    search_fields = ('user__email', 'user__username', 'major')


@admin.register(MajorOption)
class MajorOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('is_active',)
    ordering = ('name',)


@admin.register(CountryOption)
class CountryOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('is_active',)
    ordering = ('name',)
