from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UploadHistory, Equipment

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['equipment_id', 'name', 'type', 'flowrate', 'pressure', 'temperature']

class UploadHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadHistory
        fields = ['id', 'file_name', 'uploaded_at', 'total_records', 
                  'avg_flowrate', 'avg_pressure', 'avg_temperature']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user