from django.db import models
from django.conf import settings


class Profile(models.Model):
    """Extended user profile with academic, financial, and skills information"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    
    # Academic Information
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    degree_level = models.CharField(max_length=50, blank=True)  # Bachelor's, Master's, PhD
    major = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    target_country = models.CharField(max_length=100, blank=True)
    
    # Test Scores
    ielts_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    toefl_score = models.IntegerField(null=True, blank=True)
    gre_score = models.IntegerField(null=True, blank=True)
    gmat_score = models.IntegerField(null=True, blank=True)
    
    # Financial Information
    income_range = models.CharField(max_length=50, blank=True)
    need_based_preference = models.BooleanField(default=False)
    
    # Skills and Interests
    technical_skills = models.JSONField(default=list, blank=True)
    soft_skills = models.JSONField(default=list, blank=True)
    interests = models.JSONField(default=list, blank=True)
    holland_code = models.CharField(max_length=6, blank=True)  # RIASEC personality type
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'profiles'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['country', 'target_country']),
        ]
    
    def __str__(self):
        return f"Profile for {self.user.email}"

