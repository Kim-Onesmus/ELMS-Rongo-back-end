from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.Login, name='sign_in'),
    path('homepage', views.Homepage, name='homepage'),
    path('apply_leave', views.applyLeave, name='apply_leave'),
    path('download', views.Download, name='download'),
    path('history', views.History, name='history'),
    path('calendar', views.Calendar, name='calendar'),
    path('documentation', views.Documentation, name='documentation'),
    path('logout', views.Logout, name='logout'),
    path('profile', views.myProfile, name='profile'),
    path('updateProfile', views.UpdateProfile, name='updateProfile'),
    
    # <===========HR PAGES=================>
    path('all_leaves',views.allLeaves, name='all_leaves'),
    path('action/<str:pk>/', views.Action, name='action'),
    path('pending', views.Pending, name='pending'),
    path('accepted', views.Accepted, name='accepted'),
    path('rejected', views.Rejected, name='rejected'),
    
    # <===========HOD PAGES================>
    path('all_leaves1',views.allLeaves1, name='all_leaves1'),
    path('action1/<str:pk>/', views.Action1, name='action1'),
    path('pending1', views.Pending1, name='pending1'),
    path('accepted1', views.Accepted1, name='accepted1'),
    path('rejected1', views.Rejected1, name='rejected1'),
    
    # <===========Add User==================>
    path('home', views.Home, name='home'),
    path('add_user', views.addUser, name='add_user'),
    path('add_category', views.addCategory, name='add_category'),
    path('add_department', views.addDepartment, name='add_department'),
    path('jobgroup', views.JobGroup, name='jobgroup'),
    path('update_user', views.updateUser, name='update_user'),
    path('super_user', views.superUser, name='super_user'),
    path('updateSuperUser/<str:pk>/', views.UpdateSuperUser, name='updateSuperUser'),
    path('all_users', views.allUsers, name='all_users'),
    path('update_user1/<str:pk>/', views.updateUser1, name='update_user1'),
    path('delete_user/<str:pk>/', views.deleteUser, name='delete_user'),
    path('search', views.Search, name='search'),
    
    # <===========Password Reset ===========>
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="app/passwordReset/forget-password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="app/passwordReset/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="app/passwordReset/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="app/passwordReset/password_reset_done.html"), name="password_reset_complete")

]