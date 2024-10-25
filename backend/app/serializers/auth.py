from rest_framework import serializers


class SignupSerializer(serializers.Serializer):
    account_id = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
