from django.urls import path
from .views import (
    CustomerProfileCreateView,
    CustomerProfileDetailView
)

urlpatterns = [
    path("CustomerProfile/", CustomerProfileCreateView.as_view()),
    path("CustomerProfile/<int:pk>/", CustomerProfileDetailView.as_view()),
]


