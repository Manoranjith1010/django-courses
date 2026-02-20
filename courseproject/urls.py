
from django.contrib import admin
from django.urls import path, include

# To display Images
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('users/', include('apps.users.urls')),
    path('profile/', include('apps.core.urls')),  # Profile management
    path('', include('apps.courses.urls')),  # Homepage and courses at root
]
# To Display Images while onlocal server
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
