from django.db import models

class UploadHistory(models.Model):
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # Storing summary stats directly in the history model for fast retrieval
    total_records = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(null=True, blank=True)
    avg_pressure = models.FloatField(null=True, blank=True)
    avg_temperature = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.file_name} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"

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