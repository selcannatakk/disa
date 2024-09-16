from django.contrib import admin
from django.urls import path, include
from app import settings
from django.conf.urls.static import static

from disa.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)