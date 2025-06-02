from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipementTypeViewSet, EquipementViewSet, RegisterView, LoginView

router = DefaultRouter()
router.register(r'api/equipment-types', EquipementTypeViewSet)
router.register(r'api/equipment', EquipementViewSet)


urlpatterns = [path('', include(router.urls)),
               path(r'api/register', RegisterView.as_view()),
               path(r'api/login', LoginView.as_view())]

