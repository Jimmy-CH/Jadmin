
from django.urls import path
from apps.authentication.views import LoginView, CaptchaView, LogoutView

urlpatterns = [
    path('/login', LoginView.as_view(), name='login'),
    path('/captcha', CaptchaView.as_view(), name='get_captcha'),
    path('/logout', LogoutView.as_view(), name='logout'),
]

