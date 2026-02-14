from django.contrib import admin
from .models import CareerRecommendation, ModelTrainingHistory


@admin.register(CareerRecommendation)
class CareerRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'career', 'rank', 'confidence_score', 'model_used', 'created_at')
    list_filter = ('model_used', 'rank', 'created_at')
    search_fields = ('user__email', 'career__name')


@admin.register(ModelTrainingHistory)
class ModelTrainingHistoryAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'accuracy', 'precision', 'recall', 'f1_score', 'training_samples', 'trained_at')
    list_filter = ('model_name', 'trained_at')
    readonly_fields = ('trained_at',)

