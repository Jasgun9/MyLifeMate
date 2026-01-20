from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Sleep(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)  
    created_at = models.DateField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)
    def __str__(self):
        return f"duration {self.duration}"