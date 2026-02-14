"""
URL configuration for path2prep_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('profiles.urls')),
    path('api/', include('careers.urls')),
    path('api/', include('scholarships.urls')),
    path('api/', include('recommendations.urls')),
    path('api/', include('notifications.urls')),
    path('', lambda request: JsonResponse({'message': 'Path2Prep Backend API is running', 'version': '1.0.0'})),
]

# Serve media files in development
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
