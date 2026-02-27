# users/urls.py
from django.urls import path
from .views import  RegisterAPIView, LoginAPIView, UpdateRoleAPIView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('update_role/<int:pk>/', UpdateRoleAPIView.as_view(), name='update_role'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)