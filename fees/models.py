from django.db import models
from django.forms import CharField
from django.urls import reverse
from schoolinfo.models import SchoolInformation

from student.models import ClassRoom, Student

# Create your models here.
semesters=[('ft',"First Trimester"),("st","Second Trimester"),("tt","Third Trimester")]
entries=[("N","New"),("O","Old")]
    

class Fee(models.Model):
   
    receipt_no = models.CharField(
        blank=True, null=True, max_length=50, unique=True)
    student_id=models.ForeignKey(Student, on_delete=models.CASCADE,blank=True,null=True) 
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,blank=True,null=True)
    entry=models.CharField(choices=entries, max_length=50)
    semester=models.CharField(choices=semesters, max_length=50)
    total_fee=models.DecimalField(default=0.0,decimal_places=2,max_digits=15)
    amount = models.DecimalField(default=0.0,decimal_places=2,max_digits=15)
    amount_in_words = models.CharField(max_length=100,blank=True,null=True)
    due_fee=models.DecimalField(default=0.0,decimal_places=2,max_digits=15)
    fully_paid=models.BooleanField(default=False)
    partly_paid=models.BooleanField(default=False)
    date_paid=models.DateField( auto_now=True)
    updated_paid_date=models.DateTimeField( auto_now_add=True)

    

    class Meta:
        verbose_name = "Fee"
        verbose_name_plural = "Fees"

    def __str__(self):
        return str(self.student_id)

    def get_absolute_url(self):
        return reverse("Fee_detail", kwargs={"pk": self.pk})

class Receipt(models.Model):
    name=models.CharField( max_length=50)
    image=models.ImageField(upload_to='receipts')
    fee=models.ForeignKey(Fee, on_delete=models.CASCADE)

    

   
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class OnlineFeesOnProgress(models.Model):
    ref_id=models.CharField(max_length=150)
    token=models.CharField(max_length=600,blank=True,null=True)
    student_id=models.ForeignKey(Student, on_delete=models.CASCADE,blank=True,null=True) 
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,blank=True,null=True)
    entry=models.CharField(choices=entries, max_length=50)
    semester=models.CharField(choices=semesters, max_length=50)
    phone=models.CharField(max_length=15,blank=True,null=True)
    amount = models.DecimalField(default=0.0,decimal_places=2,max_digits=15)
    status=models.BooleanField(default=False)
    amount_in_words = models.CharField(max_length=100,blank=True,null=True)
    created_time=models.TimeField( auto_now_add=True)
    
    def __str__(self):
        return str(self.ref_id)+" "+str(self.student_id)
        # pass

class ServicesTokenStorage(models.Model):
    name=models.CharField( max_length=50)
    token=models.CharField( max_length=650)
    created_time=models.TimeField( auto_now_add=True)