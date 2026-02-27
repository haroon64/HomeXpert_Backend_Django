from django.db import models

# Create your models here. 

class Service(models.Model):
    service_name=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    service_icon = models.ImageField(upload_to='service_icons/', null=True, blank=True)
    
   
class SubService(models.Model):
    FIXED='F'
    NEGOTIABLE='N'

    PRICE_TYPE_CHOICES=[
        (FIXED,'Fixed Price'), 
        (NEGOTIABLE,'Negotiable Price')
    ]
    
    service=models.ForeignKey(Service,on_delete=models.CASCADE,related_name="Services")
    sub_service_name=models.CharField(max_length=255)
    description=models.TextField()
    price=models.DecimalField(max_digits=8,decimal_places=2)
    price_bargain=models.CharField(choices=PRICE_TYPE_CHOICES,default=FIXED,max_length=1)
    active_status=models.BooleanField(default=True)             
    VendorProfile=models.ForeignKey("profiles.VendorProfile",on_delete=models.CASCADE,related_name="sub_services")
    Service_image=models.ImageField(upload_to='service_images/', null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class Category(models.Model):
    sub_service_name=models.CharField(max_length=255)
    service=models.ForeignKey(Service,on_delete=models.CASCADE,related_name="categories")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Address(models.Model):
    address=models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    SubService=models.OneToOneField(SubService,on_delete=models.CASCADE,related_name="addresses")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"