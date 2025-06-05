from django_filters import rest_framework as filters
from .models import Equipment, EquipmentType
class EquipmentFilter(filters.FilterSet):
    serial_number = filters.CharFilter(lookup_expr='icontains')
    note = filters.CharFilter(lookup_expr='icontains')
    equipment_type = filters.NumberFilter(field_name='equipment_type_id')
    
    class Meta:
        model = Equipment
        fields = ['serial_number', 'note', 'equipment_type']

class EquipmentTypeFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    serial_mask =  filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = EquipmentType
        fields = ['name','serial_mask']