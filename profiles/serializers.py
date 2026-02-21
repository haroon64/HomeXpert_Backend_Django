from rest_framework import serializers
from .models import CustomerProfile

class CustomerProfileSerializer(serializers.ModelSerializer):
    # Change these from SerializerMethodField to standard fields
    # We use 'source' or just handle them in the logic
    
    class Meta:
        model = CustomerProfile
        fields = [
            "id", "full_name", "address", "phone_number", 
            "gender", "profile_image", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


    def to_internal_value(self, data):
        """
        Clean the incoming data BEFORE validation.
        """
        # 1. Handle the nested customer_profile[...] keys
        cleaned_data = {}
        for key, value in data.items():
            if key.startswith("customer_profile[") and key.endswith("]"):
                cleaned_data[key[17:-1]] = value
            else:
                cleaned_data[key] = value

        # 2. Normalize gender
        GENDER_MAP = {"male": "M", "female": "F", "other": "O"}
        gender = cleaned_data.get("gender")
        if gender and isinstance(gender, str):
            cleaned_data["gender"] = GENDER_MAP.get(gender.lower(), gender)

        # Pass the cleaned data to the actual validation logic
        return super().to_internal_value(cleaned_data)

    # This handles the GET display (replaces get_gender)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Format Gender for output
        GENDER_REVERSE_MAP = {'M': 'male', 'F': 'female', 'O': 'other'}
        representation['gender'] = GENDER_REVERSE_MAP.get(instance.gender, instance.gender)
        
        # Format Image URL for output (replaces get_profile_image)
        if instance.profile_image:
            request = self.context.get('request')
            if request:
                representation['profile_image'] = request.build_absolute_uri(instance.profile_image.url)
            else:
                representation['profile_image'] = f"/media/{instance.profile_image.name}"
        
        return representation
    

class VendorProfileSerializer(serializers.ModelSerializer):
    # Change these from SerializerMethodField to standard fields
    # We use 'source' or just handle them in the logic
    
    class Meta:
        model = CustomerProfile
        fields = [
            "id", "full_name", "address", "phone_number", 
            "gender", "profile_image", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
