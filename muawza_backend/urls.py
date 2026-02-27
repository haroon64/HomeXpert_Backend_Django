
from django.contrib import admin
from django.urls import path
from django.urls import include
from muawza_backend import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/profiles/', include('profiles.urls')),
    path('api/services/', include('services.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns