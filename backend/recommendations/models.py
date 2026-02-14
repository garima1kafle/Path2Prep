from django.db import models
from django.conf import settings
from careers.models import Career


class CareerRecommendation(models.Model):
    """Store career recommendations for users"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='career_recommendations')
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='recommendations')
    confidence_score = models.DecimalField(max_digits=5, decimal_places=4)  # 0.0000 to 1.0000
    model_used = models.CharField(max_length=50, blank=True)  # random_forest, knn, neural_network, ensemble
    rank = models.IntegerField()  # 1, 2, or 3 for top 3
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'career_recommendations'
        unique_together = ['user', 'career', 'rank']
        indexes = [
            models.Index(fields=['user', 'rank']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.career.name} (Rank {self.rank})"


class ModelTrainingHistory(models.Model):
    """Track ML model training history"""
    model_name = models.CharField(max_length=50)  # random_forest, knn, neural_network
    accuracy = models.DecimalField(max_digits=5, decimal_places=4)
    precision = models.DecimalField(max_digits=5, decimal_places=4)
    recall = models.DecimalField(max_digits=5, decimal_places=4)
    f1_score = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    training_samples = models.IntegerField()
    model_file_path = models.CharField(max_length=500, blank=True)
    
    trained_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'model_training_history'
        ordering = ['-trained_at']
    
    def __str__(self):
        return f"{self.model_name} - {self.accuracy} accuracy ({self.trained_at})"

