from django.db import models
from users.models import User
from django.conf import settings
import os

class VendorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="vendor_profile"
    )

    full_name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255, unique=True)

    latitude = models.DecimalField(
        max_digits=10,  
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        blank=True
    )

    phone_number = models.CharField(max_length=20, unique=True)
    second_phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.user.email})"
    
class VendorPortfolio(models.Model):
    vendor_profile = models.ForeignKey(
        VendorProfile,
        on_delete=models.CASCADE,
        related_name="portfolios"
    )

    work_experience = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Portfolio #{self.id} - {self.vendor_profile}"
    

class VendorPortfolioImage(models.Model):
    portfolio = models.ForeignKey(
        VendorPortfolio,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="vendor_portfolios/")
    
    # Meta data (Rails-style)
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image {self.id} for Portfolio {self.portfolio_id}"


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile"
    )

    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)

    phone_number = models.CharField(max_length=20, unique=True)
   

    MALE = 'M'
    FEMALE= 'F'
    OTHER = 'O'
    GENDER_CHOICES=[
        (MALE,'male'),
        (FEMALE,'female'),
        (OTHER,'other')
    ]
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=MALE)

    profile_image = models.ImageField(
        upload_to='profile_images/',  # Folder inside MEDIA_ROOT
        default='profile_images/default.jpg',  # default image
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.user.email})"
