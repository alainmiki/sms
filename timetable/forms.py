from random import choices
from django import forms

from timetable.models import Period, TimeTable 
from teacher.models import Staff
from student.models import ClassRoom,Department,Subject

days=(('Mon','Monday'),('Tues','Tuesday'),('Wed','Wednesday'),("Thurs",'Thursday'),("Fri","Friday"),('Sat','Saturday'),("Sun","Sunday"))

class TimeTableForm(forms.ModelForm):
    """Form definition for TimeTable."""
    class_id = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1 id_subjects"},), help_text='Select the class to set on', )
        
    staff_id = forms.ModelChoiceField(queryset=Staff.objects.all(), widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1 id_subjects"},), help_text='Select the teacher to set on', )
        
    
    day = forms.ChoiceField( choices=days ,widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1",}), help_text="Enter the day of the class session")
        
    subject_id = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select the subject  ")
    department_id = forms.ModelChoiceField(queryset=Department.objects.all(),required=False, widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select the department or leave the way it is  ")


    class Meta:
        """Meta definition for TimeTableform."""
       

        model = TimeTable
        fields = "__all__"


class PeriodForm(forms.ModelForm):
    """Form definition for Period."""
    name=forms.CharField(max_length=20, required=True,widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1",}), help_text="Enter the period name eg first period or period1 or p1 etc")
    
    start_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1",'type':'time',}), help_text="Enter the start time of the class session")
        
    end_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1",'type':'time',}), help_text="Enter the end time of the class session")

    class Meta:
        """Meta definition for Periodform."""
        

        model = Period
        fields = '__all__'


class StaffTimetableFilterForm(forms.Form):
    
    query_set=Staff.objects.all()
    
    filter_by = forms.ModelChoiceField(queryset=query_set, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1 id_subjects", ' hx-target': "#tableContent", 'hx-post': "timetable-staff-filter", 'hx-trigger': "change"},), help_text='Select the teacher to ge his/her timetable', )
    
class ClassTimetableFilterForm(forms.Form):
    
    query_set=ClassRoom.objects.all()
    
    filter_by = forms.ModelChoiceField(queryset=query_set, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1 id_subjects", ' hx-target': "#tableContent", 'hx-post': "timetable-class-filter", 'hx-trigger': "change"},), help_text='Select the class to view timetable', )
    
    # TODO: Define form fields here
