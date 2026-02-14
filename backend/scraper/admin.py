from django.contrib import admin
from .models import ScrapingLog


@admin.register(ScrapingLog)
class ScrapingLogAdmin(admin.ModelAdmin):
    list_display = ('source_url', 'status', 'records_scraped', 'records_new', 'records_duplicate', 'started_at', 'completed_at')
    list_filter = ('status', 'started_at')
    search_fields = ('source_url', 'error_message')
    readonly_fields = ('started_at', 'completed_at')

