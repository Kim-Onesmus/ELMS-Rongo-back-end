from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime, date
from datetime import timedelta
from django.contrib import messages
from django.conf import settings
from .models import Worker, Leave, Department, jobGroup, SuperUser
from .forms import LeaveForm, WorkerForm, SuperUserForm
from django.core.mail import send_mail
from django.urls import reverse
from django.db.models import Q
# Create your views here.




def Homepage(request):
    user = request.user.worker
    leaves = Leave.objects.filter(user=user)
    
    worker = Worker.objects.all()
    all_workers = worker.count()
    
    today = datetime.now().date()
    leave_accepted = 0
    for leave in leaves:
        start = datetime.strptime(str(leave.start_date), '%Y-%m-%d').date()
        end = datetime.strptime(str(leave.end_date), '%Y-%m-%d').date()
        
        if end - start != 0:
            accepted = Leave.objects.filter(leave_status='Accepted')
            leave_accepted = accepted.count()
    
    rejected = Leave.objects.filter(leave_status='Rejected')
    leave_reject = rejected.count()
    
    pending = Leave.objects.filter(leave_status='Pending')
    leave_pending = pending.count()
    
    context = {'all_workers':all_workers,'leaves':leaves, 'leave_accepted':leave_accepted,'leave_reject':leave_reject, 'leave_pending':leave_pending,}
    return render(request, 'app/index.html', context)


def applyLeave(request):
    user = request.user.worker
    leave_days = user.leave_days
    reminder = leave_days

    if request.method == 'POST':
        user = request.user.worker
        leave_type = request.POST['leave_type']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        comment = request.POST['comment']
        
        today = datetime.now().date()
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        if start <= today:
            messages.error(request, 'You cannot apply leave for past dates')
            return redirect('apply_leave')
        if end <= today:
            messages.error(request, 'You cannot apply leave for past dates')
            return redirect('apply_leave')
        if start == end:
            messages.error(request, 'Start date and end date cannot be the same')
            return redirect('apply_leave')
        if start > end:
            messages.error(request, 'Start date cannot be greater than end date')
            return redirect('apply_leave')
        
        duration = (datetime.strptime(end_date, '%Y-%m-%d').date() - datetime.strptime(start_date, '%Y-%m-%d').date()).days
        if duration <= leave_days:
            leave_days -= duration
            user.leave_days = leave_days
            user.save()
        
            leave_details = Leave.objects.create(user=user, leave_type=leave_type, start_date=start_date,end_date=end_date, comment=comment)
            leave_details.save()
            
            subject = 'Leave Application Received - Acknowledgement'
            context = {
                'user': user,
                'leave_type': leave_type,
                'start_date': start_date,
                'end_date': end_date,
            }
            html_message = render_to_string('app/email/apply.html', context)
            plain_message = strip_tags(html_message)
            
            email = EmailMultiAlternatives(subject, plain_message, settings.EMAIL_HOST_USER, [user.email])
            email.attach_alternative(html_message, "text/html")
            email.send()
            
            messages.info(request, 'Leave application submited successfully')
            return redirect('apply_leave')
        else:
            messages.error(request, 'Not enough leave days available')
            return redirect('apply_leave')
    
    
    context = {'reminder':reminder}
    return render(request, 'app/apply_leave.html', context)


def Download(request):
    user = request.user.worker
    leaves = Leave.objects.filter(user=user)
    
    total = 0
    for leave in leaves:
        duration = (leave.end_date - leave.start_date).days + 1
        total += duration
    
    context = {'leaves':leaves, 'total':total}
    return render(request, 'app/download.html', context)

def History(request):
    user = request.user.worker
    leaves = Leave.objects.filter(user=user)
    
    context = {'leaves':leaves}
    return render(request, 'app/history.html', context)

def Calendar(request):
    return render(request, 'app/calendar.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password,)
                
        if user is not None:
            auth.login(request, user)
            if username.startswith('hr2023'):
                return redirect('all_leaves')
        
            elif username.startswith('hod2023'):
                return redirect('all_leaves1')
            
            elif username.startswith('admin2023'):
                return redirect('home')
            else:
                return redirect('homepage')
        else:
            messages.error(request, 'Invalid details')
            return redirect('sign_in')
    else:
        return render(request, 'app/login.html')
    return render(request, 'app/login.html')

def Documentation(request):
    return render(request, 'app/documentation.html')

def Logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('sign_in')
        messages.info(request, 'You have been loged out')
    return render(request, 'app/logout.html')


# <=======================HR==================>

def allLeaves(request):
    leaves = Leave.objects.all()

    context = {'leaves':leaves}
    return render(request, 'app/hr/all_leaves.html', context)

def Action(request, pk):
    leaves = Leave.objects.get(id=pk)
    form = LeaveForm(instance=leaves)
    if request.method == 'POST':
        form = LeaveForm(request.POST, instance=leaves)
        if form.is_valid():
            form.save()
            
            subject = 'Leave Status'
            context = {
                'user': leaves.user,
                'leave_type': leaves.leave_type,
                'start_date': leaves.start_date,
                'end_date': leaves.end_date,
                'leave_status1':leaves.leave_status1,
            }
            
            html_message = render_to_string('app/email/hr.html', context)
            plain_message = strip_tags(html_message)
            
            email = EmailMultiAlternatives(subject, plain_message, settings.EMAIL_HOST_USER, [leaves.user.email])
            email.attach_alternative(html_message, "text/html")
            email.send()
            
            return redirect('all_leaves')
        
    context = {'form':form}
    return render(request, 'app/hr/action.html', context)

def Pending(request):
    pending = Leave.objects.filter(leave_status1='Pending')
    
    context = {'pending':pending}
    return render(request, 'app/hr/pending.html', context)

def Accepted(request):
    accepted = Leave.objects.filter(leave_status1='Accepted')
    
    context = {'accepted':accepted}
    return render(request, 'app/hr/accepted.html', context)

def Rejected(request):
    rejected = Leave.objects.filter(leave_status1='Rejected')
    
    context = {'rejected':rejected}
    return render(request, 'app/hr/rejected.html', context)


# <=======================HOD==================>

def allLeaves1(request):
    leaves = Leave.objects.all()

    context = {'leaves':leaves}
    return render(request, 'app/hod/all_leaves1.html', context)

def Action1(request, pk):
    leaves = Leave.objects.get(id=pk)
    form = LeaveForm(instance=leaves)
    if request.method == 'POST':
        form = LeaveForm(request.POST, instance=leaves)
        if form.is_valid():
            form.save()
            subject = 'Leave Status'
            context = {
                'user': leaves.user,
                'leave_type': leaves.leave_type,
                'start_date': leaves.start_date,
                'end_date': leaves.end_date,
                'leave_status':leaves.leave_status,
            }
            
            html_message = render_to_string('app/email/hod.html', context)
            plain_message = strip_tags(html_message)
            
            email = EmailMultiAlternatives(subject, plain_message, settings.EMAIL_HOST_USER, [leaves.user.email])
            email.attach_alternative(html_message, "text/html")
            email.send()
            
            return redirect('all_leaves1')
        
    context = {'form':form}
    return render(request, 'app/hod/action1.html', context)

def Pending1(request):
    pending = Leave.objects.filter(leave_status='Pending')
    
    context = {'pending':pending}
    return render(request, 'app/hod/pending1.html', context)

def Accepted1(request):
    accepted = Leave.objects.filter(leave_status='Accepted')
    
    context = {'accepted':accepted}
    return render(request, 'app/hod/accepted1.html', context)

def Rejected1(request):
    rejected = Leave.objects.filter(leave_status='Rejected')
    
    context = {'rejected':rejected}
    return render(request, 'app/hod/rejected1.html', context)

# <===============Add User ===================>

def Home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    user = Worker.objects.filter(
        Q(username__icontains=q) |
        Q(department__icontains=q) |
        Q(name__icontains=q) |
        Q(email__icontains=q)
    )
    users = user.count()
    
    all_users = Worker.objects.all()
    
    worker = Worker.objects.all()
    workers = worker.count()
    
    icts = Worker.objects.filter(department='ICT')
    ict = icts.count()
    
    finaces = Worker.objects.filter(department='FINANCE')
    finance = finaces.count()
    
    admissions = Worker.objects.filter(department='ADMISSIONS')
    admission = admissions.count()
    
    context = {'workers':workers, 'ict':ict, 'finance':finance, 'admission':admission, 'all_users':all_users, 'user':user, 'users':users}
    return render(request, 'app/addUser/home.html', context)

def allUsers(request):
    all_users = Worker.objects.all()
    
    context = {'all_users':all_users}
    return render(request, 'app/addUser/all_users.html', context)

def addUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        
        if password == password1:
            if Worker.objects.filter(username=username).exists():
                messages.error(request, 'Username exist')
                return redirect('add_user')
            elif Worker.objects.filter(email=email).exists():
                messages.error(request, 'Email exist')
                return redirect('add_user')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                client_details = Worker.objects.create(user=user, username=user.username, email=email)
                client_details.save()
                
                messages.info(request, 'Account created')
                return redirect(reverse('update_user') + '?username=' + user.username)
        else:
            messages.error(request, 'Password dont match')
            return redirect('add_user')
    return render(request, 'app/addUser/add.html')

def updateUser(request):
    username = request.GET.get('username')
    user = User.objects.get(username=username)
    worker = user.worker

    if request.method == 'POST':
        form = WorkerForm(request.POST,request.FILES, instance=worker)
        if form.is_valid():
            form.save()
            messages.info(request, 'User information updated')
            return redirect('add_user')
    else:
        form = WorkerForm(instance=worker)
    
    context = {'form': form}
    return render(request, 'app/addUser/update.html', context)


def JobGroup(request):
    if request.method == 'POST':
        job_group = request.POST['job_group']
        leaveDays = request.POST['leaveDays']
        
        if jobGroup.objects.filter(job_group=job_group).exists():
            messages.error(request, 'Job group already added')
            return redirect('jobgroup')
        else:
            jobs = jobGroup.objects.create(job_group=job_group, leaveDays=leaveDays)
            jobs.save()
            
            messages.info(request, 'Job group added')
            return redirect('jobgroup')
    else:
        return render(request, 'app/addUser/jobGroup.html')
    return render(request, 'app/addUser/jobGroup.html')


def addDepartment(request):
    if request.method == 'POST':
        department = request.POST['department']
        
        if Department.objects.filter(department=department).exists():
            messages.info(request, 'Department already exist')
            return redirect('add_department')
        else:
            departments = Department.objects.create(department=department)
            department.save()
            
            messages.info(request, 'Department added')
            return redirect('add_department')
    else:
        return render(request, 'app/addUser/department.html')
    return render(request, 'app/addUser/department.html')


def superUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        
        if password == password1:
            if Worker.objects.filter(username=username).exists():
                messages.error(request, 'Username exist')
                return redirect('super_user')
            elif Worker.objects.filter(email=email).exists():
                messages.error(request, 'Email exist')
                return redirect('super_user')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                client_details = SuperUser.objects.create(user=user, username=user.username, email=email)
                client_details.save()
                
                messages.info(request, 'Super user added')
                return redirect(reverse('updateSuperUser') + '?username=' + user.username)
        else:
            messages.error(request, 'Password dont match')
            return redirect('super_user')
    return render(request, 'app/addUser/superUser.html')

def updateSuperUser(request):
    username = request.GET.get('username')
    user = User.objects.get(username=username)
    superUser = user.superuser

    if request.method == 'POST':
        form = SuperUserForm(request.POST,request.FILES, instance=superUser)
        if form.is_valid():
            form.save()
            messages.info(request, 'Information updated')
            return redirect('super_user')
    else:
        form = SuperUserForm(instance=superUser)
    
    context = {'form': form}
    return render(request, 'app/addUser/updateSuper.html', context)



def updateUser1(request, pk):
    worker = Worker.objects.get(id=pk)
    form = WorkerForm(instance=worker)
    if request.method == 'POST':
        form = WorkerForm(request.POST,request.FILES, instance=worker)
        if form.is_valid():
            form.save()
            messages.info(request, 'User information updated')
            return redirect('all_users')
    else:
        form = WorkerForm(instance=worker)
    
    context = {'form': form}
    return render(request, 'app/addUser/update.html', context)

def deleteUser(request, pk):
    worker = Worker.objects.get(id=pk)
    if request.method == 'POST':
        worker.delete()
        return redirect('all_users')
    return render(request, 'app/addUser/delete.html', {'obj':worker})

def Search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    user = Worker.objects.filter(
        Q(username__icontains=q) |
        Q(department__icontains=q) |
        Q(section__icontains=q) |
        Q(name__icontains=q) |
        Q(email__icontains=q)
    )
    users = user.count()
    
    context = {'user':user, 'users':users}
    return render(request, 'app/addUser/search.html', context)


def myProfile(request):
    worker = request.user.worker
    
    
    context = {'worker':worker}
    return render(request, 'app/profile.html', context)


def UpdateProfile(request):
    worker = request.user.worker
    form = WorkerForm(instance=worker)
    password_form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = WorkerForm(request.POST,request.FILES, instance=worker)
        password_form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid() and password_form.is_valid():
            form.save()
            password_form.save()
            messages.info(request, 'Profile information updated')
            return redirect('profile')
    else:
        form = WorkerForm(instance=worker)
    
    context = {'form': form, 'password_form':password_form}
    return render(request, 'app/updateProfile.html', context)
