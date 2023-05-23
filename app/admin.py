from django.contrib import admin
from .models import Worker, Leave
# Register your models here.

@admin.register(Worker)
class WorkerTable(admin.ModelAdmin):
    list_display = ('name', 'department', 'job_group')
  
    
@admin.register(Leave)
class LeaveTable(admin.ModelAdmin):
    list_display = ('leave_type', 'start_date', 'end_date', 'comment', 'leave_status', 'leave_status1')