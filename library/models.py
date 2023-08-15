from django.db import models
from django.forms import DateField
from ckeditor.fields import RichTextField
from student.models import Subject
from teacher.models import Staff
# Create your models here.
from student.models import ClassRoom

class Library(models.Model):
    """Model definition for Library."""
    
    title=models.CharField(max_length=100)     
    author=models.CharField(max_length=100,blank=True,null=True)     
    poster=models.ImageField(upload_to='library',blank=True,null=True)
    subject=models.ForeignKey(Subject, on_delete=models.DO_NOTHING,blank=True,null=True)
    book=models.FileField(upload_to='library',)
    create_on=models.DateField(auto_now=True)
  
    # TODO: Define fields here

    class Meta:
        """Meta definition for Library."""

        verbose_name = 'Library'
        verbose_name_plural = 'Libraries'

    def __str__(self):
        """Unicode representation of Library."""
        return self.title


class Pass_Question(models.Model):
    """Model definition for Pass_Question."""

    # TODO: Define fields here
    
    title=models.CharField(max_length=100)
    subject=models.ForeignKey(Subject, on_delete=models.DO_NOTHING,blank=True,null=True)
    paper=models.FileField(upload_to='past questions',)
    create_on=models.DateField(auto_now=True)
    class Meta:
        """Meta definition for Pass_Question."""

        verbose_name = 'Pass_Question'
        verbose_name_plural = 'Pass_Questions'

    def __str__(self):
        """Unicode representation of Pass_Question."""
        return self.title

class DocumentOfStaff(models.Model):
    """Model definition for DocumentOfStaff."""

    # TODO: Define fields here
    title=models.CharField(max_length=100)
    author=models.CharField(max_length=100,blank=True,null=True)    
    subject=models.ForeignKey(Subject, on_delete=models.DO_NOTHING,blank=True,null=True)
    poster=models.ImageField(upload_to='library',blank=True,null=True)
    document=models.FileField(upload_to='staff document',)
    create_on=models.DateField(auto_now=True)
    class Meta:
        """Meta definition for DocumentOfStaff."""

        verbose_name = 'DocumentOfStaff'
        verbose_name_plural = 'DocumentOfStaffs'

    def __str__(self):
        """Unicode representation of DocumentOfStaff."""
        return self.title



class Assignment(models.Model):
    """Model definition for Assignment."""
    staff=models.ForeignKey(Staff, on_delete=models.DO_NOTHING,blank=True,null=True)
    class_room=models.ManyToManyField(ClassRoom,related_name='assignment_class')
    subject=models.ForeignKey(Subject, on_delete=models.DO_NOTHING,blank=True,null=True)
    submission_date=models.DateField()
    content=RichTextField()
    create_on=models.DateField(auto_now=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Assignment."""

        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'

    def __str__(self):
        """Unicode representation of Assignment."""
        return str(self.subject) + ' '+ str(self.submission_date)
