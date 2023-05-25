from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput, Select
from django.contrib.auth.models import User
from .models import Leave, Worker, Department, Category
from django import forms

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = '__all__'
        
class WorkerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reporting_to'].queryset = Worker.objects.exclude(tittle='none')
    class Meta:
        model = Worker
        fields = '__all__'
    widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control'}),
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
        'department': forms.Select(attrs={'class': 'form-control'}),
        'job_group': forms.Select(attrs={'class': 'form-control'}),
        'tittle': forms.Select(attrs={'class': 'form-control'}),
        'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        'reporting_to': forms.Select(attrs={'class': 'form-control'}),
        # Add more fields here with their respective widget styles
    }
        
        
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        # widgets = {
        #     'category': forms.Select(attrs={'class': 'form-control'}),
        # }
        
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'