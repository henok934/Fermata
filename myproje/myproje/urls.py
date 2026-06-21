"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # Include only the users app URLs
]
"""


from django.contrib import admin
from django.urls import path, include

# --- IMPORT THESE TWO FOR LOGO IMAGES ---
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')), # Your app's current routing paths
]

# --- APPEND THIS LOGIC AT THE VERY BOTTOM ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
