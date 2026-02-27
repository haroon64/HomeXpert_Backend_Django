from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ServiceSerializer,SubServiceSerializer
from .models import Service,SubService,Address

# Create your views here.
class ServiceView(ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    # def post(self,request):
    #     serializer=ServiceSerializer(data=request.data ,context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class SubServiceView(APIView):
        def post(self,request):
            serializer=SubServiceSerializer(data=request.data ,context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        def get(self,request,pk=None):
            if pk is None:
                try:
                    sub_services = SubService.objects.select_related('addresses').all()
                    serializer = SubServiceSerializer(sub_services, many=True, context={'request': request})
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except SubService.DoesNotExist:
                    return Response({'error': 'No SubServices found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                try:
                    sub_service = SubService.objects.select_related('addresses').prefetch_related('Services').get(id=pk)
                    serializer = SubServiceSerializer(sub_service, context={'request': request})
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except SubService.DoesNotExist:
                    return Response({'error': 'SubService not found'}, status=status.HTTP_404_NOT_FOUND)
                

