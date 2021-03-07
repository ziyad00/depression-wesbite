from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .forms import MessageForm
from .models import Message,Time
import datetime
import time
from django.utils import timezone
from django.utils.timezone import utc


class Home(View):
    form_class = MessageForm
    initial = {'key': 'value'}
    template_name = 'invorterapp/home.html'
    time_object = Time.objects.last()
    query = Message.objects.all()

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        if self.time_object:
            now = timezone.now()
            if self.time_object.time < now:
                Message.objects.all().delete()
                Time.objects.all().delete()
                return render(request, self.template_name, {'form': form})
            time_calculated = (self.time_object.time - timezone.now()).total_seconds()
            return render(request, self.template_name, {'form': form, 'messages':self.query, 'now':now, 'time_calculated':time_calculated})
        return render(request, self.template_name, {'form': form, 'messages':self.query})


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            time_added = datetime.timedelta(days = 7)
            if Time.objects.last():
                self.time_object.time = self.time_object.time + time_added
            else:
                time = Time.objects.create()
                time.time = time.time + time_added
                time.save()

        time_object = Time.objects.last()
        if self.time_object:
            time_calculated = (self.time_object.time - timezone.now()).total_seconds()
        else:
            time_calculated = (Time.objects.last().time - timezone.now()).total_seconds()

        form = self.form_class()
        now = timezone.now()
        return render(request, self.template_name, {'form': form, 'messages':self.query,'now':now, 'time_calculated':time_calculated})
    
         