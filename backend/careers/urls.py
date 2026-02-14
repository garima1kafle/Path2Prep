from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CareerViewSet

router = DefaultRouter()
router.register(r'careers', CareerViewSet, basename='career')

urlpatterns = router.urls

