from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Career
from .serializers import CareerSerializer


class CareerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer
    permission_classes = [AllowAny]

