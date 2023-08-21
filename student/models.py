
# from guardian.models import Guardian
from django.db import models
from django.urls import reverse
from adminhod.models import  CustomUser
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save

from ckeditor.fields import RichTextField
# from guardian.models import Guardian
entries=[("N","New"),("O","Old")]


# from student.models import ClassRoom, Department

user_types_data = (('1', "HOD"), ('2', "Staff"),
                   ('3', 'Student'), ('4', 'Guardian'))
choices = [('Mr', 'Mr'), ('Mrs', 'Mrs'), ("Sir", "Sir"), ('Prof', 'Prof'),
              ('Miss', 'Miss'), ('Misses', 'Misses'), ('Doctor', 'chief'), ('senator', "senator")]
genders=(('M',"Male"),("F","Female"),("O","Others"))

# Create your models here.
class Department(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name
    
    
class ClassRoom(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    
    class Meta:
        verbose_name = "ClassRoom"
        verbose_name_plural = "ClassRooms"

    def __str__(self):
        return self.name



class Student(models.Model):
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    entry=models.CharField(choices=entries, max_length=116,default=("N","New"))
    class_room = models.ForeignKey(
        ClassRoom, on_delete=models.DO_NOTHING, related_name="class_room", blank=True, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.DO_NOTHING, related_name="department", blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    admission_date=models.DateField(auto_now_add=True)
    
    # guardian=models.ForeignKey('Guardian',on_delete=models.DO_NOTHING,blank=True,null=True)

    

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return str(self.admin.username)

    def get_absolute_url(self):
        return reverse("Student_detail", kwargs={"pk": self.pk})

class StudentGovernment(models.Model):
    student_id=models.ForeignKey(Student, on_delete=models.CASCADE)
    position=models.CharField(max_length=50)
    created_at=models.DateField(auto_now=True)
    
    def __str__(self) -> str:
        return str(self.student_id.admin.username)
class LeaveReportStudent(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    leave_start_date = models.DateTimeField(blank=True,null=True)
    leave_end_date = models.DateTimeField(blank=True,null=True)
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.student_id.admin.username)


class FeedbackStudent(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.student_id.admin.username)


class NotificationStudent(models.Model):
    sender_name=models.CharField(max_length=100,blank=True,null=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    status=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.student_id.admin.username)


class Admission(models.Model):
    """Model definition for Admission."""

    # TODO: Define fields here
    email = models.EmailField(
        max_length=254, verbose_name='email', unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    gender = models.CharField(
        choices=genders, max_length=10, blank=True, null=True)

    place_of_birth = models.CharField(max_length=200, blank=True, null=True)

    address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    class_room = models.ForeignKey(
        ClassRoom, on_delete=models.CASCADE, related_name="admission_class_room", blank=True, null=True, default='all')
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="admission_department", blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    profile_picture = models.ImageField(
        upload_to="profile_pictures", blank=True, null=True,  max_length=100, default="static/images/default.jpg")

    user_type = models.CharField(
        default=3, choices=user_types_data, max_length=15, blank=True, null=True)

    guardian_title = models.CharField(choices=choices, max_length=10)
    guardian_full_name = models.CharField(
        max_length=100, blank=True, null=True)
    guardian_profile_picture = models.ImageField(
        upload_to="profile_pictures", blank=True, null=True,  max_length=100, default="static/images/default.jpg")

    guardian_address = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone = models.CharField(max_length=50, blank=True, null=True)
    guardian_email = models.CharField(max_length=350, blank=True, null=True)

    admission_request = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Admission."""

        verbose_name = 'Admission'
        verbose_name_plural = 'Admissions'

    def __str__(self):
        """Unicode representation of Admission."""
        return self.first_name + self.last_name


class Guardian(models.Model):
    
    
    admin=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='adminguardia', blank=True,null=True,)

    title=models.CharField(choices=choices, max_length=8)
    
    children = models.ManyToManyField(Student,related_name="student")
    
    

    class Meta:
        verbose_name = "Guardian"
        verbose_name_plural = "Guardians"

    def __str__(self):
        return str(self.admin.username)
 

    def get_absolute_url(self):
        return reverse("Guardian_detail", kwargs={"pk": self.pk})


semesters=(('ft',"first term"),('st','second term'),('tt','third term'))


class Subject(models.Model):
    name=models.CharField(max_length=50)
    coefficient=models.IntegerField(default=3)

    
    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Subject_detail", kwargs={"pk": self.pk})


# Create your models here.
class Attendance(models.Model):
    subject_id=models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    attendance_date=models.DateTimeField( auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return str(self.subject_id.name)

class AttendanceReport(models.Model):
    
    subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING,blank=True,null=True)
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE,blank=True,null=True)
    staff_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    semester=models.CharField(choices=semesters, max_length=50,default='ft')
    class_id=models.ForeignKey(ClassRoom,on_delete=models.CASCADE,blank=True,null=True)
    status=models.BooleanField(default=False)
    attendance_date=models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return str(self.student_id.admin.username)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender,instance,created, **kwargs):
    if created:
     
        if instance.user_type == '3':
            if Student.objects.filter(admin=instance).exists():
                print("Student profile user created already")
            print("Student profile user created newly")
                
            # else:
            Student.objects.create(admin=instance)


@receiver(pre_save, sender=CustomUser)
def create_user_profile(sender, instance, **kwargs):
    if not instance._state.adding:
        print('this is and update',instance.user_type)
        if instance.user_type == '3':
            g_obj=Student.objects.filter(admin=instance).exists()
            if not g_obj:
                Student.objects.create(admin=instance)
            else:
                print('exists')
    else:
        print("this is a create model",instance._state.adding)
        # if instance.user_type == '3':
        #     Student.objects.create(admin=instance)