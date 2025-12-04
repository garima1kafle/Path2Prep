from rest_framework import viewsets, permissions
from .models import User, AcademicInfo, CareerPreferences, ProfileCompletion
from .serializers import UserSerializer, AcademicSerializer, CareerPrefsSerializer, ProfileCompletionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class AcademicViewSet(viewsets.ModelViewSet):
    queryset = AcademicInfo.objects.all()
    serializer_class = AcademicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AcademicInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CareerPrefsViewSet(viewsets.ModelViewSet):
    queryset = CareerPreferences.objects.all()
    serializer_class = CareerPrefsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CareerPreferences.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProfileCompletionViewSet(viewsets.ModelViewSet):
    queryset = ProfileCompletion.objects.all()
    serializer_class = ProfileCompletionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProfileCompletion.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
