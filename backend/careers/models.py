from django.db import models


class Career(models.Model):
    """Career database for recommendations"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)  # STEM, Business, Arts, etc.
    required_skills = models.JSONField(default=list, blank=True)
    average_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    growth_rate = models.CharField(max_length=50, blank=True)  # High, Medium, Low
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'careers'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.name

