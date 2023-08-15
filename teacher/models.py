
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from adminhod.models import CustomUser
from student.models import Subject


# Create your models here.
class Staff(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                 related_name="teacher",blank=True, null=True)
   
    subjects=models.ManyToManyField(Subject, related_name="subject")
    duty_post=models.CharField(max_length=50,blank=True, null=True)
    matricule=models.CharField(max_length=150,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self) -> str:
        return str(self.admin)

class AttendanceReport(models.Model):
    staff_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="staff",blank=True,null=True)
    coming_status=models.BooleanField(default=False)
    going_status=models.BooleanField(default=False)
  
    coming_time=models.TimeField(blank=True,null=True)
    going_time=models.TimeField(blank=True,null=True)
    attendance_date=models.DateField(auto_now_add=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return str(self.staff_id.username)




class LeaveReportStaff(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_start_date = models.DateTimeField(editable=True)
    leave_end_date = models.DateTimeField(editable=True)
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self) -> str:
        return str(self.staff_id.admin)


class FeedbackStaff(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return str(self.staff_id.admin)


class NotificationStaff(models.Model):
    sender_name=models.CharField(max_length=150,blank=True,null=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    status=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return str(self.staff_id.admin.first_name)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == '2':
            Staff.objects.create(admin=instance)


# @receiver(post_save, sender=CustomUser)
# def save_user_profile(sender, instance, **kwargs):
#     pass
  
#     if instance.user_type == '2':
#         Staff.objects.create(admin=instance)
#         # instance.staff.save()
