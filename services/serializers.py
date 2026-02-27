from rest_framework import serializers
from .models import Address, SubService, Service
from drf_writable_nested.serializers import WritableNestedModelSerializer

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_name', 'service_icon', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address', 'street', 'city', 'state', 'zip_code', 'country', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SubServiceSerializer(WritableNestedModelSerializer):
    address = AddressSerializer()
    class Meta:
        model = SubService
        fields = ['id', 'service', 'sub_service_name', 'description', 'price', 'price_bargain', 'active_status', 'VendorProfile', 'Service_image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address_instance = Address.objects.create(**address_data)
        sub_service = SubService.objects.create(address=address_instance, **validated_data)
        return sub_service
    
        