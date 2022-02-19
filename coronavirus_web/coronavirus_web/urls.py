"""coronavirus_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from coronavirus_web import settings
from stats.views import parse
from index_redirect.views import index_to_stats_redirect

urlpatterns = [
    path('', index_to_stats_redirect),
    path('admin/stats/lastparsed/parse/', parse),
    path('admin/', admin.site.urls),
    path('stats/', include('stats.urls')),
    path('news/', include('news.urls')),
    path('api/', include('api.urls')),
    path('report/', include('reports.urls')),
    path('about/', include('site_info.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)