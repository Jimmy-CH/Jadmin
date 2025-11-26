
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DeptViewSet

router = DefaultRouter()
router.register(r'', DeptViewSet, basename='dept')

urlpatterns = [
    path('', include(router.urls)),
]
