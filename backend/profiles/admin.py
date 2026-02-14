from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'degree_level', 'major', 'country', 'target_country', 'gpa')
    list_filter = ('degree_level', 'country', 'target_country')
    search_fields = ('user__email', 'user__username', 'major')

