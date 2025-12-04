from rest_framework import routers
from .views import UserViewSet, AcademicViewSet, CareerPrefsViewSet, ProfileCompletionViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'academic', AcademicViewSet, basename='academic')
router.register(r'career-prefs', CareerPrefsViewSet, basename='careerprefs')
router.register(r'profile-completion', ProfileCompletionViewSet, basename='profilecompletion')

urlpatterns = router.urls
from django.urls import path, include