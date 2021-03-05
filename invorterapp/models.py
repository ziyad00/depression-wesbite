from django.db import models

class Message(models.Model):
    text = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
  
    class Meta:
        ordering = ['-created']


class Time(models.Model):
    time = models.DateTimeField(auto_now_add=True)

