from rest_framework import serializers
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