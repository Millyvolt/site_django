from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    """Health check endpoint for deployment monitoring"""
    return JsonResponse({'status': 'healthy', 'service': 'django-site'})

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
]
