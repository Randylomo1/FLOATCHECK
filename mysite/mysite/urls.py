from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mpesa/', include('mpesa_p.urls')),
    path('business/', include('business.urls')),
    path('rec/', include('rec.urls')),
    path('file-ingestion/', include('file_ingestion.urls')),
    path('integrations/', include('integrations.urls')),
    path('profile/', include('profiles.urls')),
    path('', include('core.urls')),
 ]
