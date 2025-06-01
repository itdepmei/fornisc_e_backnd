from django.db import models

# Create your models here.

class FrontendLog(models.Model):
    
    username = models.CharField(max_length=150)
    action = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.action}"
class Notification(models.Model):
    title = models.CharField(max_length=255 , default="")
    message = models.TextField()
    isRead = models.BooleanField(default=False)
    reportUuid = models.CharField(max_length=100 , default="")
    created_at = models.DateTimeField(auto_now_add=True)

