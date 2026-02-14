from django.db import models
from django.conf import settings


class Notification(models.Model):
    """User notifications"""
    NOTIFICATION_TYPES = [
        ('new_match', 'New Scholarship Match'),
        ('deadline_approaching', 'Deadline Approaching'),
        ('profile_incomplete', 'Profile Incomplete'),
        ('application_reminder', 'Application Reminder'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.URLField(blank=True)  # Optional link to related resource
    
    # Optional foreign keys
    scholarship_id = models.IntegerField(null=True, blank=True)
    application_id = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['notification_type']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"

