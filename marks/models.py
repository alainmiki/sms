from django.db import models

from teacher.models import Staff
from student.models import ClassRoom, Department, Student
from student.models import Subject
# Create your models here.

# semesters=[('ft',"first term"),('st','second term'),('tt','third term')]

semesters=[('ft',"first Trimester"),('st','second Trimester'),('tt','third Trimester')]
months=[('Jan',"January"),('Feb','February'),('Mar','March'),('Apr',"April"),('May','May'),('Jun','Jun'),('Jul',"July"),('Aug','August'),('Sep','September'),('Oct',"October"),('Nov','november'),('Dec','December'),]

class Mark(models.Model):
    student_id=models.ForeignKey(Student,related_name='student_id', on_delete=models.CASCADE)
    staff_id=models.ForeignKey(Staff,related_name='staff_id', on_delete=models.CASCADE)
    class_id=models.ForeignKey(ClassRoom,related_name='class_id', on_delete=models.CASCADE)
    subject_id=models.ForeignKey(Subject,related_name='subject_id', on_delete=models.CASCADE)
    department_id=models.ForeignKey(Department,related_name='department_id', on_delete=models.CASCADE,blank=True,null=True)
    semester=models.CharField(choices=semesters, max_length=10)
    month=models.CharField(choices=months, max_length=10,default="Sep")
    home_work=models.DecimalField(default=0,max_digits=7,decimal_places=2,blank=True,null=True)
    home_work_on=models.IntegerField(default=20,blank=True,null=True)
    test_mark=models.DecimalField(default=0,max_digits=7,decimal_places=2)
    test_on=models.IntegerField(default=20)
    project=models.DecimalField(default=0,max_digits=7,decimal_places=2,blank=True,null=True)
    project_on=models.IntegerField(default=20,blank=True,null=True)
    exam_mark=models.DecimalField(default=0,max_digits=7,decimal_places=2)
    exam_on=models.IntegerField(default=20)
    
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    
    

    class Meta:
        """Meta definition for Mark."""

        verbose_name = 'Mark'
        verbose_name_plural = 'Marks'

    def __str__(self):
        """Unicode representation of Mark."""
        return self.semester




class StudentSubjectAverageGrade(models.Model):
    """Model definition for StudentAverage."""
    student_id=models.ForeignKey(Student,related_name='student_id_grade', on_delete=models.CASCADE)
    class_id=models.ForeignKey(ClassRoom,related_name='class_id_grade', on_delete=models.CASCADE)
    semester=models.CharField(choices=semesters, max_length=50)
    average=models.DecimalField(default=0,max_digits=7,decimal_places=2)
    subject_id=models.ForeignKey(Subject,related_name='class_id_grade', on_delete=models.CASCADE)
    grade=models.CharField(max_length=3)
    
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    

    # TODO: Define fields here

    class Meta:
        """Meta definition for StudentSubjectAverageGrad."""

        verbose_name = 'StudentSubjectAverageGrad'
        verbose_name_plural = 'StudentSubjectAverageGrads'

    def __str__(self):
        """Unicode representation of StudentSubjectAverageGrad."""
        return self.student_id.admin.username + " "+ self.semester

class StudentAverage(models.Model):
    """Model definition for StudentAverage."""
    student_id=models.ForeignKey(Student,related_name='student_id_average', on_delete=models.CASCADE)
    class_id=models.ForeignKey(ClassRoom,related_name='class_id_average', on_delete=models.CASCADE)
    semester=models.CharField(choices=semesters, max_length=50)
    average=models.DecimalField(default=0,max_digits=7,decimal_places=2)
    subjects_grades=models.ManyToManyField(StudentSubjectAverageGrade, verbose_name="subjects_grade")
    
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    

    # TODO: Define fields here

    class Meta:
        """Meta definition for StudentAverage."""

        verbose_name = 'StudentAverage'
        verbose_name_plural = 'StudentAverages'

    def __str__(self):
        """Unicode representation of StudentAverage."""
        return self.student_id.admin.username + " "+ self.semester


