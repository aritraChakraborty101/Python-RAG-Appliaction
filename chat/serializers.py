from rest_framework import serializers
from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for ChatMessage model"""
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'user_message', 'ai_response', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class ChatRequestSerializer(serializers.Serializer):
    """Serializer for incoming chat requests"""
    message = serializers.CharField(max_length=5000, required=True)
    
    def validate_message(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Message cannot be empty")
        return value.strip()
