from django.urls import path
from .views import (
    CustomerProfileCreateView,
    CustomerProfileDetailView,
    VendorProfileView
)

urlpatterns = [
    path("CustomerProfile/", CustomerProfileCreateView.as_view()),
    path("CustomerProfile/<int:pk>/", CustomerProfileDetailView.as_view()),
    path("VendorProfile/", VendorProfileView.as_view()),
    path("VendorProfile/<int:pk>/", VendorProfileView.as_view()),
]


