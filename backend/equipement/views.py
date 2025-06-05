from django.shortcuts import render
from rest_framework import viewsets
from .models import Equipment, EquipmentType
from .serializers import EquiepementTypeSerializer, EquipementSerializer, LoginSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Регистрация нового пользователя
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'detail': 'Пользователь успешно зарегистрирован'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Авторизация пользователя
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Кастомный классы пагинации
class EquipmentTypePagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 10000

class EquipmentPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000

class EquipementTypeViewSet(viewsets.ModelViewSet):
    queryset = EquipmentType.objects.all()
    serializer_class = EquiepementTypeSerializer
    permission_classes = [IsAuthenticated]
    #pagination_class = EquipmentTypePagination
    
    def create(self, request, *args, **kwargs):
        data = request.data.get('items', request.data)
        many = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer=serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class EquipementViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipementSerializer
    permission_classes = [IsAuthenticated]
    #pagination_class = EquipmentPagination
    
    def create(self, request, *args, **kwargs):
        data = request.data.get('items', request.data)
        many = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer=serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
