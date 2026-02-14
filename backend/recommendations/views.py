from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .ml_engine import CareerRecommendationEngine
from .models import CareerRecommendation
from .serializers import CareerRecommendationSerializer


class CareerRecommendationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def recommend(self, request):
        """
        POST /api/recommend-career/recommend/
        Returns top 3 career recommendations based on user profile
        """
        try:
            engine = CareerRecommendationEngine()
            top_k = request.data.get('top_k', 3)
            recommendations = engine.get_recommendations(request.user, top_k=top_k)
            
            # Store recommendations in database
            CareerRecommendation.objects.filter(user=request.user).delete()
            for idx, rec in enumerate(recommendations, 1):
                CareerRecommendation.objects.create(
                    user=request.user,
                    career=rec['career'],
                    confidence_score=rec['confidence'],
                    model_used=rec.get('model', 'ensemble'),
                    rank=idx
                )
            
            return Response({
                'top_careers': [
                    {
                        'career': rec['career'].name,
                        'confidence': float(rec['confidence']),
                        'description': rec['career'].description,
                        'category': rec['career'].category,
                    }
                    for rec in recommendations
                ]
            }, status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            return Response(
                {'error': str(e), 'traceback': traceback.format_exc()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def my_recommendations(self, request):
        """Get stored recommendations for the user"""
        recommendations = CareerRecommendation.objects.filter(
            user=request.user
        ).order_by('rank')
        serializer = CareerRecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)

