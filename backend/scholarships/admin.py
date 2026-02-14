from django.contrib import admin
from .models import Scholarship, Application, Bookmark


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'country', 'deadline', 'is_approved', 'is_active', 'created_at')
    list_filter = ('is_approved', 'is_active', 'country', 'deadline')
    search_fields = ('title', 'organization', 'description', 'eligibility')
    actions = ['approve_scholarships', 'reject_scholarships']
    
    def approve_scholarships(self, request, queryset):
        queryset.update(is_approved=True, is_active=True)
    approve_scholarships.short_description = "Approve selected scholarships"
    
    def reject_scholarships(self, request, queryset):
        queryset.update(is_approved=False, is_active=False)
    reject_scholarships.short_description = "Reject selected scholarships"


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'scholarship', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'scholarship__title')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'scholarship', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'scholarship__title')

