from django.db import models
from teacher.models import Staff
from student.models import ClassRoom,Department,Subject



# Create your models here.

days=(('Mon','Monday'),('Tues','Tuesday'),('Wed','Wednesday'),("Thurs",'Thursday'),("Fri","Friday"),('Sat','Saturday'),("Sun","Sunday"))

class TimeTable(models.Model):
    """Model definition for TimeTable."""
    staff_id=models.ForeignKey(Staff,on_delete=models.CASCADE)
    class_id=models.ForeignKey(ClassRoom,on_delete=models.CASCADE)
    subject_id=models.ForeignKey(Subject,on_delete=models.CASCADE)
    department_id=models.ForeignKey(Department,on_delete=models.CASCADE,blank=True,null=True)
    day=models.CharField(max_length=6,choices=days,default=1)
   
    
    created_date=models.DateTimeField(auto_now=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for TimeTable."""
        # unique_together=['staff_id','class_id',"day",'subject_id']

        verbose_name = 'TimeTable'
        verbose_name_plural = 'TimeTables'

    def __str__(self):
        """Unicode representation of TimeTable."""
        return str (self.staff_id.admin.username)


class Period(models.Model):
    """Model definition for Period."""
    name=models.CharField(max_length=50)
    start_time=models.TimeField()
    end_time=models.TimeField()

    # TODO: Define fields here

    class Meta:
        """Meta definition for Period."""

        verbose_name = 'Period'
        verbose_name_plural = 'Periods'

    def __str__(self):
        """Unicode representation of Period."""
        return self.name



class FinalTimetable(models.Model):
    """Model definition for FinalTimetable."""
    class_id=models.ForeignKey(ClassRoom,on_delete=models.CASCADE,blank=True,null=True)
    day=models.CharField(max_length=6,choices=days,default=1)
    staff_table=models.ForeignKey(TimeTable ,on_delete=models.CASCADE)
    period=models.ForeignKey(Period ,on_delete=models.CASCADE)

    # TODO: Define fields here

    class Meta:
        """Meta definition for FinalTimetable."""

        verbose_name = 'FinalTimetable'
        verbose_name_plural = 'FinalTimetables'
        # order_by=['-period']

    def __str__(self):
        """Unicode representation of FinalTimetable."""
        return self.staff_table.staff_id.admin.username
