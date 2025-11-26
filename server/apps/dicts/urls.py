
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DictViewSet

router = DefaultRouter()
router.register(r'', DictViewSet, basename='dict')

urlpatterns = [
    path('', include(router.urls)),
]
