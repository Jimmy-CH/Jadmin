from django.urls import path, include
from apps.users.views import CurrentUserView, UserViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('/me', CurrentUserView.as_view(), name='current_user'),
    path('', include(router.urls)),
]

