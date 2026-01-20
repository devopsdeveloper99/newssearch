"""
URL configuration for web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import os
from pathlib import Path

urlpatterns = [
    path('', include('news.urls')),
    path('admin/', admin.site.urls),
]

# Serve static files
if settings.DEBUG:
    # Development: Django serves static files automatically
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Production: Serve static files through Django as fallback
    # This ensures static files work even if Apache/.htaccess doesn't handle them
    
    # Try STATIC_ROOT first (collected static files)
    if os.path.exists(settings.STATIC_ROOT):
        urlpatterns += [
            re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        ]
    else:
        # Fallback: serve directly from app static directory
        BASE_DIR = Path(__file__).resolve().parent.parent
        news_static = BASE_DIR / 'news' / 'static'
        if news_static.exists():
            urlpatterns += [
                re_path(r'^static/(?P<path>.*)$', serve, {'document_root': str(news_static)}),
            ]