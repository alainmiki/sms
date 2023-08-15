from django.contrib import admin

from timetable.models import FinalTimetable, Period, TimeTable

# Register your models here.

admin.site.register(TimeTable)
admin.site.register(Period)
# admin.site.register(FinalTimetable)
@admin.register(FinalTimetable)
class FinalTimetableAdmin(admin.ModelAdmin):
    list_display=['class_id','day',"staff_table",'period']
