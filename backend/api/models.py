from django.db import models
from django.contrib.auth.models import User 

class UploadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads') 
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Stats
    total_records = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(null=True, blank=True)
    avg_pressure = models.FloatField(null=True, blank=True)
    avg_temperature = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.file_name}"

class Equipment(models.Model):
    upload = models.ForeignKey(UploadHistory, on_delete=models.CASCADE, related_name='equipments')
    equipment_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    def __str__(self):
        return f"{self.name} ({self.type})"