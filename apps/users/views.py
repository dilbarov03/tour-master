from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .serializers import UserSerializer, SendCodeSerializer, VerifyCodeSerializer
from .verification import send_code, verify_code_cache


class MyProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class SendCodeView(generics.GenericAPIView):
    serializer_class = SendCodeSerializer
    throttle_classes = (AnonRateThrottle,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.data.get("phone")
        success, message = send_code(phone)
        if success:
            return Response({"message": message}, status=200)
        return Response({"error": message}, status=400)


class VerifyCodeView(generics.GenericAPIView):
    serializer_class = VerifyCodeSerializer
    throttle_classes = (AnonRateThrottle,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.data.get("phone")
        code = serializer.data.get("code")
        success, message = verify_code_cache(phone, code)
        if success:
            return Response({"message": message}, status=200)
        return Response({"error": message}, status=400)
