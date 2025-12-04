from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # username, email, password available from AbstractUser
    full_name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.email or self.username

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
