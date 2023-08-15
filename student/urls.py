from django.urls import path
from . import views
app_name='student'
urlpatterns = [
    path('register-student',views.RegisterStudent.as_view(),name='register-student'),
    path('edit-student/<int:c_id>/<int:id>',
         views.RegisterStudent.as_view(), name='edit-student'),
    path('delete-student/<int:pk>',views.deleteStudent,name='delete-student'),
    path('manage-student',views.manageStudents,name='manage-student'),
    path('student-student', views.StudentProfile, name='profile'),
    
    
    path('send-student-notification',
         views.SendSpecialNotification.as_view(), name='notify-student'),
    
    path('send-students-notification',
         views.SendGeneralNotification.as_view(), name='notify-students'),

    path('student-apply-leave',
         views.StudentApplyLeave.as_view(), name='student-apply-leave'),
    
    path('manage-student-leaves',
         views.ManageApproveStudentsLeaves.as_view(), name='manage-student-leaves'),

    path('edit-leaves/<int:id>', views.change_leave_status, name="edit-leaves"),
    
    path('edit-leaves-unapproved/<int:id>', views.change_leave_status_unapproved,
         name="edit-leaves-unapproved"),
    
    path('add-class',views.ClassRoomAdd.as_view(),name='add-class'),
    
    path('add-department',views.DepartmentRoomAdd.as_view(),name='add-department'),
    
    path('delete-item/<str:type_arg>/<int:id>',
         views.deleteClassOrDepartment, name='delete-item'),
    
    path('student-profile',views.StudentProfile, name='profile'),
    
    path('student-attendance',views.student_attendance_report, name='attendance'),
    
    path('filter-by',views.filterBy, name='filter-by'),
    
    path('filter-attendance',views.filter_attendance, name='filter-attendance'),
    
    path('student-marks-record',views.student_marks_record, name='student-marks-record'),
    path('filter-marks',views.student_mark_filter, name='filter-marks'),
    path('student-filter-by',views.Student_filterBy, name='student-filter-by'),
    path('homework',views.homework, name='homework'),
    path('student-government',views.create_Student_government.as_view(), name='student-government'),
    path('update_student-government/<int:id>',views.create_Student_government.as_view(), name='update_student-government'),
    path('delete_student-government/<int:id>',views.delete_Student_government, name='delete_student-government'),
    
    path('admission', views.AdmissionView.as_view(), name="admission"),
    
    
]

