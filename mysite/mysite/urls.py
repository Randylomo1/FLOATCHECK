from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mpesa/', include('apps.mpesa_p.urls')),
    path('business/', include('apps.business.urls')),
    path('rec/', include('apps.rec.urls')),
    path('file-ingestion/', include('file_ingestion.urls')),
    path('integrations/', include('apps.integrations.urls')),
    path('', include('apps.core.urls')),
]
