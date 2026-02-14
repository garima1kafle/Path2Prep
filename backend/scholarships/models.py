from django.db import models
from django.conf import settings


class Scholarship(models.Model):
    """Scholarship information from scraping"""
    title = models.CharField(max_length=500)
    organization = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    eligibility = models.TextField(blank=True)
    deadline = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    funding_amount = models.CharField(max_length=100, blank=True)  # Can be range or specific
    link = models.URLField(blank=True)
    
    # Admin approval
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Scraping metadata
    source_url = models.URLField(blank=True)
    scraped_at = models.DateTimeField(auto_now_add=True)
    mongo_id = models.CharField(max_length=100, blank=True)  # Reference to MongoDB raw data
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'scholarships'
        indexes = [
            models.Index(fields=['is_approved', 'is_active']),
            models.Index(fields=['deadline']),
            models.Index(fields=['country']),
            models.Index(fields=['title']),
        ]
    
    def __str__(self):
        return self.title


class Application(models.Model):
    """Track student scholarship applications"""
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'applications'
        unique_together = ['user', 'scholarship']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['scholarship']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.scholarship.title}"


class Bookmark(models.Model):
    """Bookmarked scholarships by students"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='bookmarks')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'bookmarks'
        unique_together = ['user', 'scholarship']
        indexes = [
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user.email} bookmarked {self.scholarship.title}"

