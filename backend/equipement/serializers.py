from rest_framework import serializers
import re
from .models import Equipment, EquipmentType
from django.core.exceptions import ValidationError

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
        print(attrs)
        mask = attrs['equipment_type'].serial_mask
        serial_number = attrs['serial_number']
        validate_serial_number(serial_number, mask)
        return attrs