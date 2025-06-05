from django.db import models
from django.db.models import Manager, QuerySet

class EquipmentManager(Manager):
    def get_queryset(self):
        return QuerySet(self.model, using=self.db).exclude(is_deleted=True)

class EquipmentType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование типа"
    )
    serial_mask = models.CharField(
        max_length=50,
        verbose_name="Маска серийного номера"
    )
    is_deleted = models.BooleanField(default=False)

    def delete(self):
        if self.is_deleted == False:
            self.is_deleted = True
            self.save()
            return True
        return False
    
    objects = EquipmentManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип оборудования"
        verbose_name_plural = "Типы оборудования"


class Equipment(models.Model):
    id = models.AutoField(primary_key=True)
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.CASCADE,
        verbose_name="Тип оборудования"
    )
    serial_number = models.CharField(
        max_length=100,
        verbose_name="Серийный номер"
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Примечание"
    )
    is_deleted = models.BooleanField(default=False)

    def delete(self):
        if self.is_deleted == False:
            self.is_deleted = True
            self.save()
            return True
        return False

    objects = EquipmentManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['equipment_type', 'serial_number'],
                name='unique_equipment_serial'
            )
        ]
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        

    def __str__(self):
        return f"{self.equipment_type.name} ({self.serial_number})"
