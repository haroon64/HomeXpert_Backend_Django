from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import CustomerProfile,VendorProfile,VendorPortfolio,VendorPortfolioImage
from collections import defaultdict
import re
from django.db import transaction

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
    

class VendorPortfolioImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPortfolioImage
        fields = ["id", "image"]

class VendorPortfolioSerializer(WritableNestedModelSerializer):
    work_images = VendorPortfolioImageSerializer(many=True, required=False)

    class Meta:
        model = VendorPortfolio
        fields = ["id", "work_experience", "work_images"]

class VendorProfileSerializer(WritableNestedModelSerializer):
    
    vendor_portfolios = VendorPortfolioSerializer(
        many=True,
        required=True
    )
    class Meta:
        model = VendorProfile
        fields = [
            "id", "full_name", "address", "phone_number",
            "second_phone_number",
            "latitude", "longitude",
            "profile_image",
            "vendor_portfolios",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
    def create(self, validated_data):
        portfolios_data = validated_data.pop("vendor_portfolios", [])

        with transaction.atomic():
            # Create VendorProfile first
            vendor_profile = VendorProfile.objects.create(**validated_data)

            # Create portfolios manually
            for portfolio_data in portfolios_data:
                images_data = portfolio_data.pop("work_images", [])

                portfolio = VendorPortfolio.objects.create(
                    vendor_profile=vendor_profile,
                    **portfolio_data
                )

                for image_data in images_data:
                    VendorPortfolioImage.objects.create(
                        portfolio=portfolio,
                        **image_data
                    )

        return vendor_profile

    def to_internal_value(self, data):
        """
        Clean the incoming multipart/form-data BEFORE validation.
        """
        formatted_data = {}
        portfolios = defaultdict(lambda: {"work_images": []})

        for key in data.keys():
            values = (
                data.getlist(key)
                if hasattr(data, "getlist")
                else (data[key] if isinstance(data[key], list) else [data[key]])
            )

            # -----------------------------
            # 1️⃣ Simple vendor_profile[field]
            # -----------------------------
            simple_match = re.match(r'vendor_profile\[(\w+)\]$', key)
            if simple_match:
                formatted_data[simple_match.group(1)] = values[0]
                continue
            
            # -----------------------------
            # 2️⃣ Portfolio fields (INCLUDING [] cases)
            # -----------------------------
            portfolio_match = re.match(
                r'vendor_profile\[vendor_portfolios_attributes\]\[(\d+)\]\[(\w+)\](?:\[\])?$',
                key
            )

            if portfolio_match:
                index = int(portfolio_match.group(1))
                field = portfolio_match.group(2)

                # ✅ Handle images properly
                if field == "work_images":
                    for file_obj in values:
                        if file_obj:
                            portfolios[index]["work_images"].append({
                                "image": file_obj
                            })

                # Ignore empty keep_image_ids
                elif field == "keep_image_ids":
                    continue

                else:
                    portfolios[index][field] = values[0]

        if portfolios:
            formatted_data["vendor_portfolios"] = list(portfolios.values())
        print("======> Formatted data for validation:", formatted_data)

        return super().to_internal_value(formatted_data)