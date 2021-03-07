
from django.db import models
from django.forms import ModelForm
from .models import Message

class MessageForm(ModelForm):
  

    class Meta:
        model = Message
        fields = '__all__'
        labels = {
            'text': '',
        }
        