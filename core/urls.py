
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from core import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('greatkartapp.urls')),
] 

# ✅ CORRECT: Only add media serving when DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
