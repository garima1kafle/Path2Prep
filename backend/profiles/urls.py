from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, MajorOptionViewSet, CountryOptionViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'options/majors', MajorOptionViewSet, basename='major-option')
router.register(r'options/countries', CountryOptionViewSet, basename='country-option')

urlpatterns = router.urls

