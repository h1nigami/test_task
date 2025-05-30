from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipementTypeViewSet, EquipementViewSet

router = DefaultRouter()
router.register(r'equipment-types', EquipementTypeViewSet)
router.register(r'equipment', EquipementViewSet)

urlpatterns = path('', include(router.urls)),

