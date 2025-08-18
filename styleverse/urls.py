from django.contrib import admin
from django.urls import path, include

# 🧠 Required to serve media files in development:
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('accounts/', include('accounts.urls')),  
 
]

# 👇 This serves uploaded media files (like product images) in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)