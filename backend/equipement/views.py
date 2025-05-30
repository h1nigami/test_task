from django.shortcuts import render
from rest_framework import viewsets
from .models import Equipment, EquipmentType
from .serializers import EquiepementTypeSerializer, EquipementSerializer
from rest_framework.permissions import IsAuthenticated

class EquipementTypeViewSet(viewsets.ModelViewSet):
    queryset = EquipmentType.objects.all()
    serializer_class = EquiepementTypeSerializer
    permission_classes = [IsAuthenticated]

class EquipementViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipementSerializer
    permission_classes = [IsAuthenticated]

