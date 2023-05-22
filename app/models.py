from django.db import models
from django.contrib.auth.models import User

# Create your models here.


DEPARTMENT = [
    ('ICT','ICT'),
    ('FINANCE','FINANCE'),
    ('ADMISSIONS','ADMISSIONS'),
]
SECTION = [
    ('PLANNING','PLANNING'),
    ('SYSTEM','SYSTEM'),
    ('MAINTENANCE','MAINTENANCE'),
]

STATUS = [
    ('Accepted','Accepted'),
    ('Rejected','Rejected'),
    ('Pending', 'Pending'),
]

class Worker(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    department = models.CharField(max_length=200, null=True, choices=DEPARTMENT)
    section = models.CharField(max_length=200, null=True, choices=SECTION)
    leave_days = models.PositiveIntegerField(default=20, null=True)
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    
class Leave(models.Model):
    user = models.ForeignKey(Worker, null=True,on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=200)
    start_date = models.DateField(max_length=200)
    end_date = models.DateField(max_length=200)
    comment = models.CharField(max_length=200)
    leave_status = models.CharField(max_length=200, choices=STATUS, default='Pending')
    leave_status1 = models.CharField(max_length=200, choices=STATUS, default='Pending')
    
    def __str__(self):
        return self.leave_type