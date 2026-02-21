from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from users.models import User
from .models import CustomerProfile,VendorProfile,VendorPortfolio,VendorPortfolioImage
from .serializers import CustomerProfileSerializer,VendorProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class CustomerProfileCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
         # Check for duplicate
        if CustomerProfile.objects.filter(user=request.user).exists():
            return Response({"error": "Profile already exists"}, status=400)

        # The serializer now handles all that looping and gender mapping automatically!
        serializer = CustomerProfileSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CustomerProfileDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        profile = get_object_or_404(CustomerProfile, user=pk)
        serializer = CustomerProfileSerializer(profile,context={'request': request})
        response_data = {
            'exists': True,
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        profile = get_object_or_404(CustomerProfile, user=pk)
        print("======> Updating profile for:", profile)


        serializer = CustomerProfileSerializer(
            profile,
            data=request.data,
            partial=False,
            context={'request': request} # allows partial update
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class VendorProfileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
      
        profile = get_object_or_404(VendorProfile, user=pk)
        serializer = VendorProfileSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
         # Check for duplicate
        if VendorProfile.objects.filter(user=request.user).exists():
            return Response({"error": "Profile already exists"}, status=400)
        print("======> Creating vendor profile for:", request.user)
        


        # The serializer now handles all that looping and gender mapping automatically!
        serializer = VendorProfileSerializer(data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)