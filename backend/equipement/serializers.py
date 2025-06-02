from rest_framework import serializers
import re
from .models import Equipment, EquipmentType
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if not user:
            raise serializers.ValidationError('Неверные учетные данные')
        if not user.is_active:
            raise serializers.ValidationError('Пользователь деактивирован')
        return user
    


VALIDATION_MAP = {
    'N': r'[0-9]',  
    'A': r'[A-Z]',  
    'a': r'[a-z]',  
    'X': r'[A-Z0-9]',  
    'Z': r'[-_@]',  
}

def validate_serial_mask(value):
    # Проверяем, что все символы маски валидны
    for char in value:
        if char not in VALIDATION_MAP:
            raise ValidationError(f"Недопустимый символ в маске: {char}")

def validate_serial_number(serial_number, mask):
    # Создаем регулярное выражение на основе маски
    pattern = f"^{''.join(VALIDATION_MAP[char] for char in mask)}$"
    
    # Проверяем соответствие серийного номера маске
    if not re.match(pattern, serial_number):
        raise ValidationError(
            "Серийный номер не соответствует заданной маске"
        )

class EquiepementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = '__all__'

    def validate_serial_mask(self, data):
        validate_serial_mask(data)
        return data

class EquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

    def validate(self, attrs):
        mask = attrs['equipment_type'].serial_mask
        serial_number = attrs['serial_number']
        validate_serial_number(serial_number, mask)
        return attrs