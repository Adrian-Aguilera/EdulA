from rest_framework import serializers
from .models import ChatHistory
class ChatHistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = '__all__'