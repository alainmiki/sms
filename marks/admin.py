from django.contrib import admin

from .models import Mark,StudentAverage,StudentSubjectAverageGrade

# Register your models here.

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'class_id', 'staff_id', 'semester']
    list_display_links=['student_id', 'class_id', 'staff_id', 'semester']

admin.site.register(StudentSubjectAverageGrade)
admin.site.register(StudentAverage)