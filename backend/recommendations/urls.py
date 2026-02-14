from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CareerRecommendationViewSet

router = DefaultRouter()
router.register(r'recommend-career', CareerRecommendationViewSet, basename='career-recommendation')

urlpatterns = router.urls

