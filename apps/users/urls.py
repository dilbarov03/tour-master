from django.urls import path

from .views import MyProfileAPIView, SendCodeView, VerifyCodeView

urlpatterns = [
    path('my-profile/', MyProfileAPIView.as_view(), name='my-profile'),
    path('send-code/', SendCodeView.as_view(), name='send-code'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
]
