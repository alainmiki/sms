
from django import forms

from student.models import Subject

from student.models import ClassRoom, Department, Student
from teacher.models import Staff
from .models import Mark

# semesters=[('ft',"first term"),('st','second term'),('tt','third term')]
semesters=[('ft',"first Trimester"),('st','second Trimester'),('tt','third Trimester')]
months=[('Jan',"January"),('Feb','February'),('Mar','March'),('Apr',"April"),('May','May'),('Jun','Jun'),('Jul',"July"),('Aug','August'),('Sep','September'),('Oct',"October"),('Nov','november'),('Dec','December'),]


class markgenFormAdmin(forms.Form):
    
    staff_id = forms.ModelChoiceField(queryset=Staff.objects.all(), label="Staff", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select the teacher who is teaching this subject")
    
    class_id = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), label="Class", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select class")

    subject_id = forms.ModelChoiceField(queryset=Subject.objects.all(), label="Subject", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select subject of the marks")
    
    department_id = forms.ModelChoiceField(queryset=Department.objects.all(), label="Department", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select department. you can leave it blank if the subject is a general subject",required=False)
    
    semester = forms.ChoiceField(label="Trimester", choices=semesters, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select semester in which marks are to be recorded')
    
    month = forms.ChoiceField(label="Month", choices=months, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select month in which marks are to be recorded')
    
    
    
class markgenForm(forms.Form):
    semesters=[('ft',"first Trimester"),('st','second Trimester'),('tt','third Trimester')]
    # staff_id = forms.ModelChoiceField(queryset=Staff.objects.all(), label="Staff", widget=forms.Select(
    #     attrs={"class": "form-control"}), help_text="Select the teacher who is teaching this subject")
    
    class_id = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), label="Class", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select class")

    subject_id = forms.ModelChoiceField(queryset=Subject.objects.all(), label="Subject", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select subject of the marks")
    
    department_id = forms.ModelChoiceField(queryset=Department.objects.all(), label="Department", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select department. you can leave it blank if the subject is a general subject",required=False)
    
    semester = forms.ChoiceField(label="Trimester", choices=semesters, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select semester in which marks are to be recorded')
    
    month = forms.ChoiceField(label="Month", choices=months, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select month in which marks are to be recorded')
    

class MarkForm(forms.ModelForm):
    
   
    """Form definition for Mark."""
    student_id = forms.ModelChoiceField(queryset=Student.objects.all(), label="Student", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select Student to which marks are to be assign ")

    staff_id = forms.ModelChoiceField(queryset=Staff.objects.all(),required=False, label="Staff", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select the teacher who is teaching this subject")
    
    class_id = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), label="Class", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select class")

    subject_id = forms.ModelChoiceField(queryset=Subject.objects.all(), label="Subject", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select subject of the marks")
    
    semester = forms.ChoiceField(label="Trimester", choices=semesters, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select select semester in which marks are to be recorded')
    
    test_mark = forms.DecimalField(initial=0, max_digits=7, decimal_places=2, widget=forms.NumberInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}))
    test_overall = forms.IntegerField(initial=20, widget=forms.NumberInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}))
    exam_mark=forms.DecimalField(initial=0,max_digits=7,decimal_places=2,widget=forms.NumberInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}))
    exam_overall = forms.IntegerField(initial=20, widget=forms.NumberInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}))


    class Meta:
        """Meta definition for Markform."""

        model = Mark
        fields = "__all__"


class FilterFormAdmin(forms.Form):

    classes = [('all', 'all'), ]
    try:
         for class_r in ClassRoom.objects.all():
            classes.append((class_r.name, class_r.name))
    except :
        pass
    
    choices_list1 = [('all', 'all'), ('staff',
                                      'staff'),('class',
                                      'class'), ('subject', 'subject'), ('student', 'student'), ('semester', 'semester'),('department', 'department'),('month', 'month'), ]
    
    choices_list = [('all', 'all'),('id', 'id'), ('class_id',
                                      'class_id'), ('subject_id', 'subject_id'), ('student_id', 'student_id'), ('department_id', 'department_id'), ('semester', 'semester'),('month', 'month'), ]
    # ('first name', 'first name'), ('last name', 'last name'), 

    filter_by = forms.ChoiceField(label="Filter by ", choices=choices_list1, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", ' hx-target': "#get_by", 'hx-swap': 'outerHtml', 'hx-post': "filter-by", 'hx-trigger': "change"}), required=True, help_text='Select filter type on or allow the default as all', initial=choices_list1[0])
    

    get_by = forms.ChoiceField(label="Get By", choices=[], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", ' hx-target': "#tableContent", 'hx-post': "filter-marks", 'hx-trigger': "change"}), required=False, help_text='Select the data category or allow the default as all', initial=choices_list1[0])
    
    class_room = forms.ChoiceField(label="Class", choices=classes, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1 ", ' hx-target': "#tableContent", 'hx-post': "filter-marks", 'hx-trigger': "change"}), required=True, help_text='Select the data category of a specific class or allow the default as all')

    sort_by = forms.ChoiceField(label="sort by", choices=choices_list, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1 sort_by", ' hx-target': "#tableContent", 'hx-post': "filter-marks", 'hx-trigger': "change"}), required=True, help_text='Select a filter by option to continue the filtering or allow the default as all', initial=choices_list[0])
 
class FilterForm(forms.Form):

    classes = [('all', 'all'), ]
    try:
         for class_r in ClassRoom.objects.all():
            classes.append((class_r.name, class_r.name))
    except :
        pass
    
    choices_list1 = [('all', 'all'), ('class',
                                      'class'), ('subject', 'subject'), ('student', 'student'), ('semester', 'semester'),('department', 'department'),('month', 'month'), ]
    
    choices_list = [('all', 'all'),('id', 'id'), ('class_id',
                                      'class_id'), ('subject_id', 'subject_id'), ('student_id', 'student_id'), ('department_id', 'department_id'), ('semester', 'semester'),('month', 'month'), ]
    # ('first name', 'first name'), ('last name', 'last name'), 

    filter_by = forms.ChoiceField(label="Filter by ", choices=choices_list1, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", ' hx-target': "#get_by", 'hx-swap': 'outerHtml', 'hx-post': "filter-by", 'hx-trigger': "change"}), required=True, help_text='Select filter type on or allow the default as all', initial=choices_list1[0])
    

    get_by = forms.ChoiceField(label="Get By", choices=[], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", ' hx-target': "#tableContent", 'hx-post': "filter-marks", 'hx-trigger': "change"}), required=False, help_text='Select the data category or allow the default as all', initial=choices_list1[0])
    
    class_room = forms.ChoiceField(label="Class", choices=classes, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1 ", ' hx-target': "#tableContent", 'hx-post': "filter-marks", 'hx-trigger': "change"}), required=True, help_text='Select the data category of a specific class or allow the default as all')

    sort_by = forms.ChoiceField(label="sort by", choices=choices_list, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1 sort_by", ' hx-target': "#tableContent", 'hx-post': "filter-marks", 'hx-trigger': "change"}), required=True, help_text='Select a filter by option to continue the filtering or allow the default as all', initial=choices_list[0])
 

class ReportCardForm(forms.Form):
    staff_id = forms.ModelChoiceField(queryset=Staff.objects.all(),required=True, label="Class Teacher", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select a class teacher who is responsible for the class")
     
    class_id = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), label="Class", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select class")
    
   
    semester = forms.ChoiceField(label="Trimester", choices=semesters, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select select semester in which report card is to be recorded')
    
    
    
    report_type = forms.ChoiceField(label="Report Type", choices=[['monthly',"Monthly"],['trimester',"Trimester"]], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select select report type in which report card is to be made')
    
    month = forms.ChoiceField(label="Month", choices=months, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select month in which reports are to be made')
    
    
    