from rest_framework import serializers
from .models import *

class FrontendLogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FrontendLog
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta:
        model = Notification
        fields = '__all__'