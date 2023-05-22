from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput, Select
from django.contrib.auth.models import User
from .models import Leave, Worker
from django import forms

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = '__all__'
        
class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = '__all__'