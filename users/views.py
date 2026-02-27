# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer,RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import User


class LoginAPIView(APIView):
    permission_classes = []  # allow any user to login

    def post(self, request):
        print("Login request data:", request.data)
       
        serializer = LoginSerializer(data=request.data['user'])
        print("Login serializer data:", serializer.initial_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            "token": str(refresh.access_token),
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        }, status=status.HTTP_200_OK)
    
class RegisterAPIView(APIView):
    permission_classes = []  # anyone can register

    def post(self, request):
        serializer = RegisterSerializer(data=request.data['user'])
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
          
        }, status=status.HTTP_201_CREATED)

class UpdateRoleAPIView(APIView):
    
    def patch(self, request,pk):
        user = get_object_or_404(User, id=pk)
        print(f"Current user: {user.email}, current role: {user.role}")
        print("Request data for role update:", request.data)
        new_role = request.data.get('role')
        print(f"Updating role for user {user.email} to {new_role}")

        if new_role not in ['customer', 'vendor']:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.role = new_role
        user.save()
        return Response({"message": "Role updated successfully"}, status=status.HTTP_200_OK)