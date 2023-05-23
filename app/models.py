from django.db import models
from django.contrib.auth.models import User

# Create your models here.


DEPARTMENT = [
    ('ICT','ICT'),
    ('FINANCE','FINANCE'),
    ('ADMISSIONS','ADMISSIONS'),
]
TITTLE = [
    ('vc','Vice Chancellor'),
    ('dvc', 'Deputy Vice Chancellor'),
    ('hod','Head Of Department'),
    ('hr','Human Resource'),
]

STATUS = [
    ('Accepted','Accepted'),
    ('Rejected','Rejected'),
    ('Pending', 'Pending'),
]
class jobGroup(models.Model):
    job_group = models.CharField(max_length=10)
    leaveDays = models.PositiveIntegerField()
    
    def __str__(self):
        return self.job_group
    
class Department(models.Model):
    department = models.CharField(max_length=200)
    
    def __str__(self):
        return self.department

class SuperUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    department = models.OneToOneField(Department, null=True, on_delete=models.CASCADE)
    job_group = models.OneToOneField(jobGroup, null=True, on_delete=models.CASCADE)
    tittle = models.CharField(max_length=200, null=True, choices=TITTLE)
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    

class Worker(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    department = models.CharField(max_length=200, null=True, choices=DEPARTMENT)
    job_group = models.OneToOneField(jobGroup, null=True, on_delete=models.CASCADE)
    # leave_days = models.PositiveIntegerField(default=20, null=True)
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