from django.db import models

from student.models import Student
from teacher.models import Staff

# Create your models here.

class NotificationStudent(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationStaff(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(Staff,on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
