from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScholarshipViewSet, ApplicationViewSet, BookmarkViewSet

router = DefaultRouter()
router.register(r'scholarships', ScholarshipViewSet, basename='scholarship')
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')

urlpatterns = router.urls

