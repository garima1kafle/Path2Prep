from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from .models import Profile, MajorOption, CountryOption
from .serializers import ProfileSerializer, MajorOptionSerializer, CountryOptionSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get', 'patch', 'put'])
    def me(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        if request.method in ['PATCH', 'PUT']:
            serializer = self.get_serializer(profile, data=request.data, partial=(request.method == 'PATCH'))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class MajorOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """Public list of majors for dropdown selection"""
    queryset = MajorOption.objects.filter(is_active=True)
    serializer_class = MajorOptionSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None  # Return all options without pagination


class CountryOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """Public list of countries for dropdown selection"""
    queryset = CountryOption.objects.filter(is_active=True)
    serializer_class = CountryOptionSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None  # Return all options without pagination

