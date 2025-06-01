from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

# محضر كشف واظهار الاثار الجرمية في مسرح الجريمة 

class Incident(models.Model):
    uuid = models.CharField(max_length=255, unique=True, blank=True, null=True)
    date_discovery = models.TextField(default="" , null=True, blank=True)
    accident_date = models.TextField(default="" ,null=True, blank=True)
    investigating_body = models.CharField(max_length=255, default="")
    accident_description = models.TextField(default="")
    inspection_time = models.TextField(null=True, blank=True)
    accident_location = models.TextField( null=True, blank=True)
    accident_city = models.CharField(max_length=255, null=True, blank=True)
    action_taken = models.TextField(null=True, blank=True)
    method = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, default='local')
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    typeAccident = models.CharField(max_length=100, null=True, blank=True)
    resulting_damages = models.TextField(null=True, blank=True)
    causes_of_fire = models.TextField(null=True, blank=True)
    category_accident = models.CharField(
        max_length=20,
        choices=[('fireAccident', 'Fire Accident'), ('accident', 'Accident')],
        default='accident'
    )
    user = models.ForeignKey(CustomUser, related_name='accidents', on_delete=models.CASCADE, null=True, blank=True)
    send_to_admin = models.BooleanField(default=False)
    updated_at_offline = models.TextField(null=True, blank=True)
    created_at_offline = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Accident {self.uuid} - {self.status}"

# images
class IncidentImage(models.Model):
    accident_uuid = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='incidents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


    
class Evidence(models.Model):
        uuid = models.CharField(max_length=255, unique=True, blank=True, null=True)
        accident_uuid = models.CharField(max_length=255, null=True, blank=True)
        sampleType = models.CharField(max_length=255, null=True, blank=True)
        sampleNumber = models.CharField(max_length=255, null=True, blank=True)
        Placeoflifting = models.CharField(max_length=255, null=True, blank=True)
        metodeIifting = models.CharField(max_length=255, null=True, blank=True)
        status = models.CharField(max_length=50, default='local')
        userId = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
        created_at = models.DateTimeField(default=timezone.now)
        updated_at = models.DateTimeField(auto_now=True)
        def __str__(self):
            return f"AccidentSample {self.id} - {self.sample_type} ({self.status})"

# لجنة الشكاوي
class Complaint(models.Model):
    uuid = models.CharField(max_length=255, unique=True, blank=True, null=True)    
    section_uuid = models.CharField(max_length=255, null=True, blank=True)  
    name = models.CharField(max_length=255 , null=True, blank=True)
    section_id = models.CharField(max_length=255, null=True, blank=True)
    position = models.TextField(null=True, blank=True)
    rank = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, default='local')
    userId = models.CharField(null=True, blank=True)
    isHidden  = models.BooleanField(default=False)
    updated_at_offline = models.TextField(null=True, blank=True)
    created_at_offline = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Accident Section {self.id} - {self.name} ({self.status})"



# استمارة استلام و تسليم العينات

class InspectionForm(models.Model):
    uuid = models.CharField(max_length=255, unique=True, blank=True, null=True)
    # form_id = models.ForeignKey('Incident', on_delete=models.CASCADE, related_name='inspection_forms' , null=True, blank=True)
    form_uuid = models.CharField(max_length=255, null=True, blank=True)
    isChemistryLab = models.BooleanField(default=True)
    isWeaponsLab = models.BooleanField(default=True)
    isForensicLab = models.BooleanField(default=False)
    isCriminalPrint = models.BooleanField(default=False)
    isDNALab = models.BooleanField(default=False)
    isCriminalElectronic = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default='local')
    userId = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        
        return f"SampleDetail {self.id} - Status: {self.status}"


