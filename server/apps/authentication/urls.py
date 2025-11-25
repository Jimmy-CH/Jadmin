# urls.py (项目根 urls.py 或 app 的 urls.py)
from django.urls import path
from .views import LoginView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
]

