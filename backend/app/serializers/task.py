from rest_framework import serializers


class TaskManagementSerializer(serializers.Serializer):
    user_prompt = serializers.CharField(max_length=255)
    chat_history = serializers.ListField()
    is_generated = serializers.BooleanField(default=False)
