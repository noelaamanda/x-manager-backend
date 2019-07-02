from rest_framework import serializers
from chat.models import Chat, Documents
from django.contrib.auth.models import User 

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('__all__')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = "__all__"