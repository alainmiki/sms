# from student.models import Student
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save


from adminhod.models import CustomUser
from student.models import Guardian


# Create your models here.


class NotificationGuardian(models.Model):
    sender_name=models.CharField(max_length=100,blank=True,null=True)
    guardian_id = models.ForeignKey(Guardian, on_delete=models.CASCADE)
    message = models.TextField()
    status=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.guardian_id.admin.username)


# @receiver(post_save, sender=CustomUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     # print(instance._state)
#     if created:
#         if instance.user_type == '4':
            
#             Guardian.objects.create(admin=instance)
      
# @receiver(pre_save, sender=CustomUser)
# def create_user_profile(sender, instance, **kwargs):
#     if not instance._state.adding:
#         print('this is and update',instance.user_type)
#         if instance.user_type == '4':
#             g_obj=Guardian.objects.filter(admin=instance).exists()
#             if not g_obj:
#                 Guardian.objects.create(admin=instance)
#             else:
#                 print('existes')
#     else:
#         print("this is a create model",instance._state.adding)
#         # if instance.user_type == '4':
#         #     Guardian.objects.create(admin=instance)
      
