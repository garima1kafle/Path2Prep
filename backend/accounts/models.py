from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom User model with role-based access"""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    
    # username, email, password available from AbstractUser
    full_name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    is_email_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return self.email or self.username
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_student(self):
        return self.role == 'student'

class AcademicInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='academic')
    education_level = models.CharField(max_length=50, blank=True)
    field_of_study = models.CharField(max_length=100, blank=True)
    gpa = models.CharField(max_length=10, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    institution = models.CharField(max_length=255, blank=True)

class CareerPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='career_prefs')
    career_interests = models.JSONField(default=list, blank=True)
    preferred_destinations = models.JSONField(default=list, blank=True)

class ProfileCompletion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_completion')
    skills = models.TextField(blank=True)
    financial_need = models.CharField(max_length=100, blank=True)
    career_goals = models.TextField(blank=True)
    agreed_to_terms = models.BooleanField(default=False)
