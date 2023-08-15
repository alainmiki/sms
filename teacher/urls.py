from django import views
from django.urls import path
from django.urls import path
from .import views
app_name="teacher"
urlpatterns = [
    path('',views.registration.as_view(),name='register'),
    path('manage-staffs', views.manage_staffs.as_view(), name='manage-staffs'),
    path('edit-staffs/<int:c_id>/<int:id>', views.update_staff.as_view(), name='edit-staffs'),
    path('send-staff-notification', views.SendSpecialNotification.as_view(), name='notify-staff'),
    path('send-staffs-notification',
         views.SendGeneralNotification.as_view(), name='notify-staffs'),
    
     path('staff-apply-leave',
          views.StaffApplyLeave.as_view(), name='staff-apply-leave'),
     path('manage-staff-leaves',
          views.ManageAproveStaffsLeaves.as_view(), name='manage-staff-leaves'),
     
    path('edit-leaves/<int:id>', views.change_leave_status, name="edit-leaves"),
    path('edit-leaves-unapproved/<int:id>', views.change_leave_status_unapprove,
         name="edit-leaves-unapproved"),
    
    path('assignment-create',views.CreateAssignment.as_view(),name='assignment-create'),
    path('assignment-update/<int:id>',views.CreateAssignment.as_view(),name='assignment-update'),
    path('staff-daily-attendance',views.create_daily_staff_attendance,name='staff-daily-attendance'),
    path('staff-daily-attendance_status_update/<int:t_id>/<int:id>',views.StaffAttendance_statu_update,name='attendance_status_update'),
    path('profile-staff',views.profile,name='profile'),
]


