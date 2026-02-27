from django.urls import path
from .views import ServiceView, SubServiceView

urlpatterns = [
    path('services/', ServiceView.as_view({'get': 'list', 'post': 'create'}), name='service-list'),
    path('subservices/', SubServiceView.as_view()),
    path('subservices/<int:pk>/', SubServiceView.as_view()),
]