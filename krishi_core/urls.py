from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import farmers.urls
import buyers.urls
import experts.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('produce/', include('produce.urls')),
    
    # Template URLs
    path('farmers/', include(farmers.urls.template_urlpatterns)),
    path('experts/', include(experts.urls.template_urlpatterns)),
    path('buyers/', include(buyers.urls.template_urlpatterns)),
    
    # API URLs
    path('api/farmers/', include('farmers.urls')),
    path('api/buyers/', include('buyers.urls')),
    path('api/experts/', include('experts.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('produce/', include('produce.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
