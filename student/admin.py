from django.contrib import admin

from student.models import Admission, Attendance, AttendanceReport, ClassRoom, Department, FeedbackStudent, LeaveReportStudent, NotificationStudent, Student, StudentGovernment, Subject

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ['admin',"department_id", 'class_room',]
    list_display_links = ['admin',"department_id", 'class_room']
    ordering = ['admin']
    

admin.site.register(Student,StudentAdmin)
admin.site.register(LeaveReportStudent)
admin.site.register(FeedbackStudent)
admin.site.register(NotificationStudent)
admin.site.register(Department)
admin.site.register(ClassRoom)
admin.site.register(Admission)


# Register your models here.
@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'subject_id',
                    'class_id', 'attendance_date', 'status']
    # list_edit=['student_id','subject_id','class_id','status']
    


admin.site.register(Subject)
admin.site.register(Attendance)
admin.site.register(StudentGovernment)

