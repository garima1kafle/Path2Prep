from rest_framework import serializers
from .models import CareerRecommendation, ModelTrainingHistory
from careers.serializers import CareerSerializer


class CareerRecommendationSerializer(serializers.ModelSerializer):
    career = CareerSerializer(read_only=True)
    
    class Meta:
        model = CareerRecommendation
        fields = '__all__'
        read_only_fields = ('user', 'created_at')


class ModelTrainingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTrainingHistory
        fields = '__all__'
        read_only_fields = ('trained_at',)

