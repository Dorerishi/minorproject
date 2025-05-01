from django.db import models

class ScanResult(models.Model):
    patient_name = models.CharField(max_length=100)
    file_name = models.CharField(max_length=200)
    prediction = models.CharField(max_length=50)
    confidence = models.FloatField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # New fields
    fhir_patient_id = models.CharField(max_length=100, blank=True, null=True)
    fhir_observation_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.patient_name} - {self.prediction}"
