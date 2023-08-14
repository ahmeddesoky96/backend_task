
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from document_processing.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('document_processing.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
