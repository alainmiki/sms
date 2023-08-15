from django.contrib import admin

from teacher.models import AttendanceReport, FeedbackStaff, LeaveReportStaff, NotificationStaff, Staff

# Register your models here.

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display=['admin','matricule']
    list_display_links = ['admin', 'matricule']


@admin.register(LeaveReportStaff)
class LeaveReportStaffAdmin(admin.ModelAdmin):
    pass
    
@admin.register(FeedbackStaff)
class FeedbackStaffAdmin(admin.ModelAdmin):
    pass

@admin.register(NotificationStaff)
class NotificationStaffAdmin(admin.ModelAdmin):
    pass
@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    pass

