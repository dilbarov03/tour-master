from rest_framework import serializers

from .models import User


class RegionBranchSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    region = RegionBranchSerializer()
    branch = RegionBranchSerializer()

    class Meta:
        model = User
        fields = ('id', 'full_name', 'region', 'branch', 'phone')


class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)


class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    code = serializers.IntegerField(required=True)
