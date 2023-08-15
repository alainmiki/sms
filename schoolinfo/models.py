
from django.db import models
from django.urls import reverse

from ckeditor.fields import RichTextField

# Create your models here.
class SchoolInformation(models.Model):
    school_name_abbreviation=models.CharField(max_length=50,blank=True,null=True)
    school_name_full=models.CharField(max_length=350,blank=True,null=True)
    address=models.CharField(max_length=350)
    email=models.CharField(max_length=350)
    phone=models.CharField(max_length=350)
    fee_phone=models.CharField(max_length=350,blank=True,null=True)
    whatsApp=models.CharField(max_length=350)
    website=models.CharField(max_length=350)
    # website=models.CharField(max_length=350)
    new_student_fee=models.FloatField(default=0.0)
    old_student_fee=models.FloatField(default=0.0)
    school_logo=models.ImageField(upload_to='logo',max_length=500)
    h_o_s_signature=models.ImageField(upload_to='signature',max_length=500,blank=True,null=True,)
    school_stamp=models.ImageField(upload_to='stamp',max_length=500,blank=True,null=True,default='images/banner.png',)
    school_banner_image=models.ImageField(upload_to='banner',blank=True,null=True,max_length=500,default='images/banner.png')
    motto=models.CharField(max_length=350)
    description=RichTextField(blank=True,null=True)
    history=RichTextField(blank=True,null=True)
    region=models.CharField(max_length=350)
    town=models.CharField(max_length=350)
    po_box=models.CharField(max_length=350)

    

    class Meta:
        verbose_name = "SchoolInformation"
        verbose_name_plural = "Schoolinformation's"

    def __str__(self):
        return self.school_name_abbreviation

    def get_absolute_url(self):
        return reverse("SchoolInformation_detail", kwargs={"pk": self.pk})


class Activity(models.Model):
    """Model definition for Activity."""

    # TODO: Define fields here
    name=models.CharField(max_length=100,blank=True,null=True)
    description=models.TextField(blank=True,null=True)
    
    created_date=models.DateTimeField( auto_now=True)
    class Meta:
        """Meta definition for Activity."""

        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __str__(self):
        """Unicode representation of Activity."""
        return self.name
