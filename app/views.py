from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from datetime import datetime, timedelta, date
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.http  import Http404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime, date
from django.http import JsonResponse
from datetime import timedelta
from django.contrib import messages
from django.conf import settings
from .models import Worker, Leave, Department, jobGroup, Category
from .forms import LeaveForm, WorkerForm, DepartmentForm, CategoryForm, jobGroupForm
from django.core.mail import send_mail
from django.urls import reverse
from django.db.models import Q
# Create your views here.

kenya_holidays = [
    date(2023, 1, 1),  # New Year's Day
    date(2023, 4, 7),  # Good Friday
    date(2023, 4, 10),  # Easter Monday
    date(2023, 5, 1),  # Labor Day
    date(2023, 6, 1),  # Madaraka Day
    date(2023, 10, 20),  # Mashujaa Day
    date(2023, 12, 12),  # Jamhuri Day
    date(2023, 12, 25),  # Christmas Day
    date(2023, 12, 26),  # Boxing Day
]
def is_weekend(date):
    return date.weekday() >= 5  # Saturday = 5, Sunday = 6

def is_holiday(date):
    return date in kenya_holidays


@login_required(login_url='/')
def Homepage(request):
    user = request.user.worker

    # Get leaves for the logged-in user
    leaves = Leave.objects.filter(user=user)
    total_leaves = leaves.count()

    # Count leave status for the logged-in user
    leave_accepted = leaves.filter(leave_status='Accepted', leave_status1='Accepted').count()
    leave_reject = leaves.filter(leave_status='Rejected', leave_status1='Rejected').count()
    leave_pending = leaves.filter(leave_status='Pending', leave_status1='Pending').count()

    # Get other data you need (e.g., total workers)
    worker = Worker.objects.all()
    all_workers = worker.count()

    context = {
        'all_workers': all_workers,
        'leaves': leaves,
        'leave_accepted': leave_accepted,
        'leave_reject': leave_reject,
        'leave_pending': leave_pending,
        'total_leaves': total_leaves
        
    }
    return render(request, 'app/index.html', context)


@login_required(login_url='/')
def applyLeave(request):
    worker = request.user.worker
    user = request.user.worker
    # leave = Leave.objects.filter(user=user)
    available_leave_days = worker.leave_days

    if request.method == 'POST':
        leave_type = request.POST['leave_type']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        duties = request.POST['number']
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

        worker_duties = Worker.objects.filter(user__username=duties).first()
        if not worker_duties:
            messages.error(request, 'Invalid PF number')
            return redirect('apply_leave')
        
        duration = (end - start).days + 1

        if duration <= available_leave_days:

            leave_details = Leave.objects.create(user=worker, leave_type=leave_type, start_date=start_date, end_date=end_date, duties=duties, comment=comment)
            leave_details.save() 
            
            
            subject = 'Leave Application Received - Acknowledgement'
            context = {
                'user': worker,
                'leave_type': leave_type,
                'start_date': start_date,
                'end_date': end_date,
            }
            html_message = render_to_string('app/email/apply.html', context)
            plain_message = strip_tags(html_message)

            email = EmailMultiAlternatives(subject, plain_message, settings.EMAIL_HOST_USER, [worker.email])
            email.attach_alternative(html_message, "text/html")
            email.send()
                
            messages.info(request, 'Leave application submitted successfully')
            return redirect('apply_leave')

        else:
            messages.error(request, 'Not enough leave days available')
            return redirect('apply_leave')

    context = {'reminder': available_leave_days}
    return render(request, 'app/apply_leave.html', context)



@login_required(login_url='/')
def Download(request):
    user = request.user.worker
    leaves = Leave.objects.filter(user=user)
    
    total = 0
    for leave in leaves:
        duration = (leave.end_date - leave.start_date).days + 1
        total += duration
    
    context = {'leaves':leaves, 'total':total}
    return render(request, 'app/download.html', context)

@login_required(login_url='/')
def History(request):
    user = request.user.worker
    leaves = Leave.objects.filter(user=user)
    
    context = {'leaves':leaves}
    return render(request, 'app/history.html', context)


@login_required(login_url='/')
def CarryForward(request):
    worker = request.user.worker
    reminder = worker.leave_days
    carry_forwarded = worker.leave_days_previous_year
    total_leave_days = worker.leave_days + worker.leave_days_previous_year
    context = {
        'reminder': reminder,
        'carry_forwarded': carry_forwarded,
        'total_leave_days': total_leave_days
    }
    return render(request, 'app/carryForward.html', context)

@login_required(login_url='/')
def Calendar(request):
    return render(request, 'app/calendar.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password,)
                
        if user is not None:
            auth.login(request, user)
            if username.startswith('Admin'):
                return redirect('home')

            elif request.user.worker.tittle == 'vc':
                return redirect('all_leaves1')
            
            elif request.user.worker.tittle == 'dean':
                return redirect('all_leaves1')
            
            elif request.user.worker.tittle == 'dvc':
                return redirect('all_leaves1')
            
            elif request.user.worker.tittle == 'hod':
                return redirect('all_leaves1')
            
            elif request.user.worker.tittle == 'hr':
                return redirect('all_leaves')
            
            else:
                return redirect('homepage')
        else:
            messages.error(request, 'Invalid details')
            return redirect('sign_in')
    else:
        return render(request, 'app/login.html')
    return render(request, 'app/login.html')

@login_required(login_url='/')
def Documentation(request):
    return render(request, 'app/documentation.html')

@login_required(login_url='/')
def Logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.info(request, 'You have been loged out')
        return redirect('sign_in')
    return render(request, 'app/logout.html')


@login_required(login_url='/')
def Search1(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    leave = Leave.objects.filter(
        Q(leave_type__icontains=q) |
        Q(start_date__icontains=q) |
        Q(end_date__icontains=q)
    )

    context = {'leave':leave}
    return render(request, 'app/search1.html', context)

# <=======================HR==================>

@login_required(login_url='/')
def allLeaves(request):
    leaves = Leave.objects.filter(leave_status='Accepted')
    rejected = leaves.filter(leave_status1='Rejected')
    pending = leaves.filter(leave_status1='Pending')
    accepted = leaves.filter(leave_status1='Accepted')
    
    leave_count = leaves.count()
    rejected_count = rejected.count()
    pending_count = pending.count()
    accepted_count = accepted.count()
    
    context = {
        'leaves':leaves,
        "leave_count":leave_count,
        'rejected_count': rejected_count,
        'pending_count':pending_count,
        'accepted_count':accepted_count,
        }
    return render(request, 'app/hr/all_leaves.html', context)


@login_required(login_url='/')
def Action(request, pk):
    leave = Leave.objects.get(id=pk)
    form = LeaveForm(instance=leave)
    worker = leave.user
    available_leave_days = worker.leave_days

    if request.method == 'POST':
        form = LeaveForm(request.POST, instance=leave)
        if form.is_valid():
            leave_status_before = leave.leave_status1  
            form.save()

            if leave.leave_status1 == 'Accepted':
                start_date = leave.start_date
                end_date = leave.end_date
                start = datetime.strptime(str(start_date), '%Y-%m-%d').date()
                end = datetime.strptime(str(end_date), '%Y-%m-%d').date()
                
                duration = (end - start).days + 1

                leave_days = 0
                for i in range(duration):
                    current_date = start + timedelta(days=i)
                    if not is_weekend(current_date) and not is_holiday(current_date):
                        leave_days += 1

                if leave_days <= available_leave_days:
                    worker.leave_days -= leave_days
                    worker.save()
                else:
                    messages.error(request, 'Not enough leave days available')
                    return redirect('all_leaves')

            subject = 'Leave Status'
            context = {
                'user': leave.user,
                'leave_type': leave.leave_type,
                'start_date': leave.start_date,
                'end_date': leave.end_date,
                'leave_status1': leave.leave_status1,
            }

            html_message = render_to_string('app/email/hr.html', context)
            plain_message = strip_tags(html_message)

            email = EmailMultiAlternatives(subject, plain_message, settings.EMAIL_HOST_USER, [leave.user.email])
            email.attach_alternative(html_message, "text/html")
            email.send()

            messages.success(request, 'Leave status has been updated.')
            return redirect('all_leaves')

    context = {'form': form, 'reminder': available_leave_days}
    return render(request, 'app/hr/action.html', context)



@login_required(login_url='/')
def Pending(request):
    pending = Leave.objects.filter(leave_status1='Pending')
    
    context = {'pending':pending}
    return render(request, 'app/hr/pending.html', context)

@login_required(login_url='/')
def Accepted(request):
    accepted = Leave.objects.filter(leave_status1='Accepted')
    
    context = {'accepted':accepted}
    return render(request, 'app/hr/accepted.html', context)

@login_required(login_url='/')
def Rejected(request):
    rejected = Leave.objects.filter(leave_status1='Rejected')
    
    context = {'rejected':rejected}
    return render(request, 'app/hr/rejected.html', context)


# <=======================HOD==================>

@login_required(login_url='/')
def allLeaves1(request):
    hod = request.user.worker
    leaves = Leave.objects.filter(user__reporting_to=hod)
    rejected = leaves.filter(leave_status='Rejected')
    pending = leaves.filter(leave_status='Pending')
    accepted = leaves.filter(leave_status='Accepted')
    
    leave_count = leaves.count()
    rejected_count = rejected.count()
    pending_count = pending.count()
    accepted_count = accepted.count()
    
    context = {
        'leaves':leaves,
        "leave_count":leave_count,
        'rejected_count': rejected_count,
        'pending_count':pending_count,
        'accepted_count':accepted_count,
        }

    return render(request, 'app/hod/all_leaves1.html', context)

@login_required(login_url='/')
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

@login_required(login_url='/')
def Pending1(request):
    hod = request.user.worker
    pending = Leave.objects.filter(user__reporting_to=hod, leave_status='Pending')
    
    context = {'pending':pending}
    return render(request, 'app/hod/pending1.html', context)

@login_required(login_url='/')
def Accepted1(request):
    hod = request.user.worker
    accepted = Leave.objects.filter(user__reporting_to=hod, leave_status='Accepted')
    
    context = {'accepted':accepted}
    return render(request, 'app/hod/accepted1.html', context)

@login_required(login_url='/')
def Rejected1(request):
    hod = request.user.worker
    rejected = Leave.objects.filter(user__reporting_to=hod, leave_status='Rejected')
    
    context = {'rejected':rejected}
    return render(request, 'app/hod/rejected1.html', context)

# <===============Add User ===================>
@login_required(login_url='/')
def Home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    user = Worker.objects.filter(
        Q(username__icontains=q) |
        Q(name__icontains=q) |
        Q(email__icontains=q)
    )
    users = user.count()
    
    all_users = Worker.objects.all()

    job_group = jobGroup.objects.all()
    job_groups = job_group.count
    
    worker = Worker.objects.all()
    workers = worker.count()
    
    category = Category.objects.all()
    category_count = category.count()
    
    department = Department.objects.all()
    departments = department.count
    
    context = {
        'workers':workers, 
        'all_users':all_users, 
        'user':user, 
        'users':users,
        'category_count':category_count,
        'departments':departments,
        'department':department,
        'job_groups':job_groups,
        'job_group':job_group,
        }
    return render(request, 'app/addUser/home.html', context)

@login_required(login_url='/')
def allUsers(request):
    all_users = Worker.objects.all()
    
    context = {'all_users':all_users}
    return render(request, 'app/addUser/all_users.html', context)

@login_required(login_url='/')
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

@login_required(login_url='/')
def updateUser(request):
    categories = Category.objects.all()
    username = request.GET.get('username')
    user = User.objects.get(username=username)
    worker = user.worker
    
    workers = Worker.objects.exclude(tittle='none').values('pk', 'username','name')
    if request.method == 'POST':
        form = WorkerForm(request.POST,request.FILES, instance=worker)
        if form.is_valid():
            form.save()
            messages.info(request, 'User information updated')
            return redirect('add_user')
    else:
        form = WorkerForm(instance=worker)
    
    context = {'form': form, 'categories': categories,'workers': workers}
    return render(request, 'app/addUser/update.html', context)

@login_required(login_url='/')
def JobGroup(request):
    if request.method == 'POST':
        jobgroup = request.POST['job_group']
        leaveDays = request.POST['leaveDays']
        
        if jobGroup.objects.filter(jobgroup=jobgroup).exists():
            messages.error(request, 'Job group already added')
            return redirect('jobgroup')
        else:
            jobs = jobGroup.objects.create(jobgroup=jobgroup, leaveDays=leaveDays)
            jobs.save()
            
            messages.info(request, 'Job group added')
            return redirect('jobgroup')
    else:
        return render(request, 'app/addUser/jobGroup.html')
    return render(request, 'app/addUser/jobGroup.html')

@login_required(login_url='/')
def addDepartment(request):
    department_form = DepartmentForm()

    if request.method == 'POST':
        department_form = DepartmentForm(request.POST)

        if department_form.is_valid():
            department_name = department_form.cleaned_data['department']
            if Department.objects.filter(department=department_name).exists():
                messages.error(request, 'Department already exists')
            else:
                department = department_form.save(commit=False)
                department.save()
                messages.info(request, 'Submitted')
                return redirect('add_department')

    context = {
        'department_form': department_form
    }
    return render(request, 'app/addUser/department.html', context)

@login_required(login_url='/')
def updateDepartment(request, pk):
    department = Department.objects.get(id=pk)
    department_form = DepartmentForm(instance=department)

    if request.method == 'POST':
        department_form = DepartmentForm(request.POST, instance=department)

        if department_form.is_valid():
            department_name = department_form.cleaned_data['department']
            if Department.objects.filter(department=department_name).exists():
                messages.error(request, 'Department already exists')
            else:
                department = department_form.save(commit=False)
                department.save()
                messages.info(request, 'updated')
                return redirect('home')
    context = {
        'department_form': department_form
    }
    return render(request, 'app/addUser/updateDepartment.html', context)

@login_required(login_url='/')
def addCategory(request):
    category_form = CategoryForm()

    if request.method == 'POST':
        category_form = CategoryForm(request.POST)

        if category_form.is_valid():
            category_name = category_form.cleaned_data['category']
            if Category.objects.filter(category=category_name).exists():
                messages.error(request, 'Category already exists')
            else:
                category = category_form.save()
                messages.success(request, 'Category added')
                return redirect('add_category')


    context = {
        'category_form': category_form,
    }
    return render(request, 'app/addUser/category.html', context)

@login_required(login_url='/')
def updateJobGroup(request, pk):
    category = jobGroup.objects.get(id=pk)
    category_form = jobGroupForm(instance=category)

    if request.method == 'POST':
        category_form = jobGroupForm(request.POST, instance=category)

        if category_form.is_valid():
            category = category_form.save()
            messages.success(request, 'Job Group Updated')
            return redirect('home')

    context = {
        'category_form': category_form,
    }
    return render(request, 'app/addUser/updateJobGroup.html', context)

@login_required(login_url='/')
def superUser(request):
    all_users = Worker.objects.exclude(tittle='none').exclude(tittle=None)
    
    context = {'all_users':all_users}
    return render(request, 'app/addUser/superUser.html', context)

@login_required(login_url='/')
def UpdateSuperUser(request, pk):
    worker = Worker.objects.get(id=pk)
    form = WorkerForm(instance=worker)
    if request.method == 'POST':
        form = WorkerForm(request.POST,request.FILES, instance=worker)
        if form.is_valid():
            form.save()
            messages.info(request, 'User information updated')
            return redirect('super_user')
    else:
        form = WorkerForm(instance=worker)
    
    context = {'form': form}
    return render(request, 'app/addUser/updateSuper.html', context)


@login_required(login_url='/')
def updateUser1(request, pk):
    categories = Category.objects.all()
    worker = Worker.objects.get(id=pk)
    form = WorkerForm(instance=worker)
    
    workers = Worker.objects.exclude(tittle='none').values('pk', 'username','name')
    
    if request.method == 'POST':
        form = WorkerForm(request.POST,request.FILES, instance=worker)
        if form.is_valid():
            form.save()
            messages.info(request, 'User information updated')
            return redirect('all_users')
    else:
        form = WorkerForm(instance=worker)
    
    context = {'form': form, 'categories':categories,'workers': workers}
    return render(request, 'app/addUser/update.html', context)

@login_required(login_url='/')
def deleteUser(request, pk):
    worker = Worker.objects.get(id=pk)
    if request.method == 'POST':
        worker.delete()
        return redirect('all_users')
    
    context = {
        'obj':worker,
    }
    return render(request, 'app/addUser/delete.html', context)

@login_required(login_url='/')
def deleteDepartment(request, pk):
    department = Department.objects.get(id=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('home')
    
    context = {
        'department':department,
    }
    return render(request, 'app/addUser/delete.html', context)

@login_required(login_url='/')
def deleteJob(request, pk):
    job = jobGroup.objects.get(id=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('all_users')
    
    context = {
        'job':job,
    }
    return render(request, 'app/addUser/delete.html', context)

@login_required(login_url='/')
def Search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    # Search for users matching the query
    users = Worker.objects.filter(
        Q(username__icontains=q) |
        Q(name__icontains=q) |
        Q(email__icontains=q)
    )
    user_count = users.count()
    
    # Search for departments matching the query
    departments = Department.objects.filter(department__icontains=q)
    department_count = departments.count()
    
    # Search for job groups matching the query
    job_groups = jobGroup.objects.filter(jobgroup__icontains=q)
    job_group_count = job_groups.count()
    
    context = {
        'users': users,
        'user_count': user_count,
        'departments': departments,
        'department_count': department_count,
        'job_groups': job_groups,
        'job_group_count': job_group_count,
        'search_query': q
    }
    return render(request, 'app/addUser/search.html', context)

@login_required(login_url='/')
def myProfile(request):
    worker = request.user.worker
    
    context = {'worker':worker}
    return render(request, 'app/profile.html', context)

@login_required(login_url='/')
def UpdateProfile(request):
    worker = request.user.worker
    form = WorkerForm(instance=worker)
    if request.method == 'POST':
        form = WorkerForm(request.POST,request.FILES, instance=worker)
        if form.is_valid():
            form.save()
            messages.info(request, 'Profile information updated')
            return redirect('profile')
    else:
        form = WorkerForm(instance=worker)
    
    context = {'form': form}
    return render(request, 'app/updateProfile.html', context)

@login_required(login_url='/')
def UpdateProfile1(request):
    password_form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            password_form.save()
            messages.info(request, 'Profile information updated')
            return redirect('profile')
    else:
        password_form = PasswordChangeForm(request.user)
    
    context = {'password_form':password_form}
    return render(request, 'app/updateProfile.html', context)
