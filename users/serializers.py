from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid ivalid email and passwords")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid passwords")
        
        if not user.is_active:
            raise serializers.ValidationError("User is inactive")
        
        data["user"] = user
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'phone_number', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password') # pops so plain pasword is not saved
        user = User(**validated_data)
        user.set_password(password) # hashes the password
        user.save()

        # Create token automatically
      

        return user