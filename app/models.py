from django.db import models
from django.contrib.auth.models import User

# Create your models here.


DEPARTMENT = [
    ('','----select department-----'),
    ('School Of Education','School Of Education'),
    ('School Of Arts, Social Science and Business','School Of Arts, Social Science and Business'),
    ('School Of Science, Agriculture and Environmental Studies','School Of Science, Agriculture and Environmental Studies'),
    ('School Of Information Communication and Media Studies','School Of Information Communication and Media Studies'),
    ('Carriculum Instructions and Media','Carriculum Instructions and Media'),
    ('Education Psychology and Science','Education Psychology and Science'),
    ('Education Foundation and Management','Education Foundation and Management'),
    ('Humanities and Social Sciences','Humanities and Social Sciences'),
    ('Languages, Literature and Linguistics','Languages, Literature and Linguistics'),
    ('Business, Tourism and Hospitality','Business, Tourism and Hospitality'),
    ('Physical Biological and Health Sciences','Physical Biological and Health Sciences'),
    ('Mathematics, Statistics and Computing','Mathematics, Statistics and Computing'),
    ('Agriculture and Environmental Studies','Agriculture and Environmental Studies'),
    ('Information Science, Health Records and Systems','Information Science, Health Records and Systems'),
    ('Communication Media and Journalism','Communication Media and Journalism'),
    ('Research and Extensions','Research and Extensions'),
    ('Open, Distance and E-Learning','Open, Distance and E-Learning'),
    ('Quality Assurance and ISO','Quality Assurance and ISO'),
    ('Postgraduate Studies','Postgraduate Studies'),
    ('Centre for Media, Democracy, Peace and Security','Centre for Media, Democracy, Peace and Security'),
    ('Principle','Principle'),
    ('Quality Assurance','Quality Assurance'),
    ('Security','Security'),
    ('Procurement','Procurement'),
    ('Council Secretariat','Council Secretariat'),
    ('Internal Audit','Internal Audit'),
    ('Administrative Office (Office of the Vive-Chancellor)','Administrative Office (Office of the Vive-Chancellor)'),
    ('ICT','ICT'),
    ('Legal Services','Legal Services'),
    ('Registrar, Administration and Planning','Registrar, Administration and Planning'),
    ('Human Resource','Human Resource'),
    ('Central Service and Operation','Central Service and Operation'),
    ('Hostels and Catering','Hostels and Catering'),
    ('Planning','Planning'),
    ('Development','Development'),
    ('Finance','Finance'),
    ('Finance Operations','Finance Operations'),
    ('Finance Planning','Finance Planning'),
    ('Student Finance','Student Finance'),
    ('Registrar, Academic and Affairs','Registrar, Academic and Affairs'),
    ('Admissions','Admissions'),
    ('Examinations','Examinations'),
    ('Senate Secretariat','Senate Secretariat'),
    ('Dean of Students','Dean of Students'),
    ('Music, Drama, Games and Sports','Music, Drama, Games and Sports'),
    ('Student Welfare, Career Services and Alumni','Student Welfare, Career Services and Alumni'),
    ('Library Services','Library Services'),
    ('Medical Services','Medical Services'),
]
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
    job_group = models.CharField(max_length=10)
    leaveDays = models.PositiveIntegerField()
    
    def __str__(self):
        return self.job_group
    
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
    job_group = models.ForeignKey(jobGroup, null=True, on_delete=models.CASCADE)
    tittle = models.CharField(max_length=200, choices=TITTLE, default='none', null=True)
    reporting_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', default='default.jpeg', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    
class Leave(models.Model):
    user = models.ForeignKey(Worker, null=True,on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=200)
    start_date = models.DateField(max_length=200)
    end_date = models.DateField(max_length=200)
    comment = models.CharField(max_length=200)
    duties = models.CharField(max_length=200)
    leave_status = models.CharField(max_length=200, choices=STATUS, default='Pending')
    leave_status1 = models.CharField(max_length=200, choices=STATUS, default='Pending')
    
    def __str__(self):
        return self.leave_type