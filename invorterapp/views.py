from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .forms import MessageForm
from .models import Message,Time
import datetime
from django.utils import timezone

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
            time_calculated = self.time_object.time - timezone.now()
            return render(request, self.template_name, {'form': form, 'messages':self.query,'time':self.time_object.time, 'now':now})
        return render(request, self.template_name, {'form': form, 'messages':self.query})


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            time_added = datetime.timedelta(days = 7)
            if self.time_object:
                self.time_object.time = self.time_object.time + time_added
            else:
                time = Time.objects.create()
                time.time = time.time + time_added
                time.save()
            time_calculated = self.time_object.time - timezone.now()
        form = self.form_class()
        now = timezone.now()
        return render(request, self.template_name, {'form': form,'time':self.time_object.time, 'messages':self.query,'now':now})
    
         