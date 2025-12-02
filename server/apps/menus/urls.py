
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, MenuRouteView, MenuOptionsView, MenuFormView

router = DefaultRouter()
router.register(r'', MenuViewSet, basename='menu')

urlpatterns = [
    path('routes/', MenuRouteView.as_view()),
    path('options/', MenuOptionsView.as_view()),
    path('<int:id>/form/', MenuFormView.as_view()),
    path('', include(router.urls)),  # 自动生成 /menus/ 的 CRUD
]
