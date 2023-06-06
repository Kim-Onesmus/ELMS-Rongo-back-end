from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

# Create your models here.
TITTLE = [
    ('none','None'),
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
    jobgroup = models.CharField(max_length=10)
    leaveDays = models.PositiveBigIntegerField()
        
    def __str__(self):
        return self.jobgroup
    
class Category(models.Model):
    category = models.CharField(max_length=200)
    
    def __str__(self):
        return self.category
    
class Department(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    department = models.CharField(max_length=200)
    
    def __str__(self):
        return self.department

    

class Worker(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    job_group = models.CharField(max_length=200, null=True)
    leave_days = models.PositiveBigIntegerField(default=0, null=True)
    tittle = models.CharField(max_length=200, choices=TITTLE, default='none', null=True)
    reporting_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', default='default.jpeg', null=True, blank=True)
    last_leave_year = models.PositiveIntegerField(default=0)
    leave_days_previous_year = models.PositiveBigIntegerField(default=0)
    leave_days_utilized_previous_year = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Worker)
def update_leave_days_previous_year(sender, instance, created, **kwargs):
    if created:
        # New worker created, set initial values for previous year leave tracking
        instance.last_leave_year = date.today().year - 1
        instance.leave_days_previous_year = 0
        instance.leave_days_utilized_previous_year = 0
        instance.save()
    elif instance.last_leave_year < date.today().year - 1:
        # Current year is more than 1 year ahead of last_leave_year, reset leave days to initial value
        instance.leave_days = instance.leave_days
        instance.leave_days_utilized_previous_year = 0
        instance.last_leave_year = date.today().year - 1
        instance.save()
    
    
class Leave(models.Model):
    user = models.ForeignKey(Worker, null=True,on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=200)
    start_date = models.DateField(max_length=200)
    end_date = models.DateField(max_length=200)
    comment = models.CharField(max_length=200)
    duties = models.CharField(max_length=200)
    comment1 = models.CharField(max_length=200, null=True)
    leave_status = models.CharField(max_length=200, choices=STATUS, default='Pending')
    leave_status1 = models.CharField(max_length=200, choices=STATUS, default='Pending')
    
    def __str__(self):
        return self.leave_type