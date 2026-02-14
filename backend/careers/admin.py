from django.contrib import admin
from .models import Career


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'growth_rate', 'created_at')
    list_filter = ('category', 'growth_rate')
    search_fields = ('name', 'description', 'category')

