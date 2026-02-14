from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Scholarship, Application, Bookmark
from .serializers import ScholarshipSerializer, ApplicationSerializer, BookmarkSerializer
from .nlp_matcher import ScholarshipMatcher


class ScholarshipViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Scholarship.objects.filter(is_approved=True, is_active=True)
    serializer_class = ScholarshipSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country']
    search_fields = ['title', 'organization', 'description', 'eligibility']
    ordering_fields = ['deadline', 'created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def match(self, request):
        """
        POST /api/scholarships/match/
        Returns top 5 scholarship matches based on user profile using NLP
        """
        try:
            matcher = ScholarshipMatcher()
            top_k = request.data.get('top_k', 5)
            matches = matcher.match_scholarships(request.user, top_k=top_k)
            
            return Response({
                'matches': [
                    {
                        'scholarship': ScholarshipSerializer(match['scholarship']).data,
                        'relevance_score': match['relevance_score'],
                        'method': match['method']
                    }
                    for match in matches
                ]
            }, status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            return Response(
                {'error': str(e), 'traceback': traceback.format_exc()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

