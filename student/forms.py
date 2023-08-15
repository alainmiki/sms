
from django import forms
from django.contrib.auth.forms import UserCreationForm

from guardian.models import Guardian


from .models import *


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter first name')

    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter middle and last name')

    email = forms.EmailField(label="Email Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Enter User valid email address')

    address = forms.CharField(label="Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter home address')

    place_of_birth = forms.CharField(label="Place Of Birth", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter Place of bith')

    gender = forms.ChoiceField(label="Gender", choices=[('M', 'Male'), ('F', 'Female'), ('0', "Others")], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select gender')
    
    user_type = forms.ChoiceField(label="User type", choices=[('3', "Student"),], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select user type', initial=("3", "Student"))

    phone = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={
                            'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter a working phone number')

    date_of_birth = forms.DateField(widget=forms.DateInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", 'type': "date"}), help_text="Enter the date of birth of student FORMAT: YEAR-MONTH-DAY")

    class_room = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), label="Class", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select class of student ")

    department = forms.ModelChoiceField(queryset=Department.objects.all(), label="Department", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select department of student ")
    # guardian = forms.ModelChoiceField(queryset=Guardian.objects.all(),required=False, label="Guardian", widget=forms.Select(
    #     attrs={"class": "form-control"}), help_text="Select guardian of student ")

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1",'hidden':'true'}), max_length=100,disabled=True,show_hidden_initial=False, required=False, help_text='Enter a valid secure password it should be more than 6 characters')

    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1",'hidden':'true'}), max_length=100,disabled=True,show_hidden_initial=False, required=False, help_text='Enter enter the previous password make sure it matches')
    
    
    profile_picture = forms.ImageField(label="Profile Picture",required=False, widget=forms.FileInput(attrs={'class': "custom-file-input",
                                                                                              'id': "exampleInputFile"}))

    class Meta:
        model = CustomUser
        # exclude_fields=[]
        fields = ['first_name', 'last_name', 'email', 'address', 'gender',
                  'place_of_birth', 'phone', 'user_type','password1','password2', 'profile_picture']
# 'username',


class StudentUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter first name')

    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter middle and last name')

    email = forms.EmailField(label="Email Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Enter User valid email address')

    address = forms.CharField(label="Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter home address')

    place_of_birth = forms.CharField(label="Place Of Birth", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter Place of bith')

    gender = forms.ChoiceField(label="Gender", choices=[('M', 'Male'), ('F', 'Female'), ('0', "Others")], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select gender')
    user_type = forms.ChoiceField(label="User type", choices=[('1', 'HOD'), ('2', 'Sfaff'), ('3', "Student"), ("4", "Guardian")], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select user type', initial=("3", "Student"), disabled=True)

    phone = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={
        'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter a working phone number')

    date_of_birth = forms.DateField(widget=forms.DateInput(
        attrs={'date of birth': "form-control rounded", 'id': "exampleInputEmail1", 'type': "date"}), help_text="Enter the date of birth of student FORMAT: YEAR-MONTH-DAY")

    class_room = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), label="Class", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select class of student ")

    department = forms.ModelChoiceField(queryset=Department.objects.all(), label="Department", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select department of student ")
    guardian = forms.ModelChoiceField(queryset=Guardian.objects.all(), label="Guardian", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select guardian of student ")

    class Meta:
        """Meta definition for StudentUpdateForm."""

        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'address', 'gender',
                  'place_of_birth', 'phone',  'user_type']


class StudentLeaveFormForm(forms.ModelForm):
    """Form definition for StaffLeaveForm."""
    student_id = forms.ModelChoiceField(queryset=Student.objects.all(), label="Staff name", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select who to apply leave")

    leave_start_date = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", 'type': "datetime-local"}), help_text="Enter the date and time your leave will will start")

    leave_end_date = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", 'type': "datetime-local"}), help_text="Enter the date and time your leave will expire")

    leave_message = forms.CharField(widget=forms.Textarea(
        attrs={'row': 12, 'col': 12, 'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='write the information to send')

    class Meta:
        """Meta definition for StudentLeaveFormform."""

        model = LeaveReportStudent
        fields = ('student_id', 'leave_start_date',
                  'leave_end_date', 'leave_message',)


class GenerallStudentNotificationForm(forms.Form):
    sender_name = forms.CharField(label="Sender's Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter the name of the person sending this notification or the person who ordered the sending ')
    message = forms.CharField(label="Massage", widget=forms.Textarea(
        attrs={'col': 12, 'row': 12, "class": "form-control"}), required=True, help_text='write the information to send')


class SpecificStudentNotificationForm(forms.Form):
    sender_name = forms.CharField(label="Sender's Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter the name of the person sending this notification or the person who ordered the sending ')

    student = forms.ModelChoiceField(queryset=Student.objects.all(), label="Student to noty", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select who to send notification")

    message = forms.CharField(label="Massage", widget=forms.Textarea(
        attrs={'col': 12, 'row': 12, "class": "form-control"}), required=True, help_text='write the information to send')


class ClassForm(forms.ModelForm):
    name = forms.CharField(label="Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter the name of the class')
    description = forms.CharField(label="Description", widget=forms.Textarea(
        attrs={'col': 12, 'row': 12, "class": "form-control"}), required=True, help_text='write information about this class')

    class Meta:
        model = ClassRoom
        fields = "__all__"


class DepartmentForm(forms.ModelForm):
    name = forms.CharField(label="Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter the name of the department')
    description = forms.CharField(label="Description", widget=forms.Textarea(
        attrs={'col': 12, 'row': 12, "class": "form-control"}), required=True, help_text='write information about this department')

    class Meta:
        model = Department
        fields = "__all__"


class AttendanceFilterForm(forms.Form):

    # classes = [('all', 'all'), ]
    # for class_r in ClassRoom.objects.all():
    #     classes.append((class_r.name, class_r.name))


    choices_list1 = [('all', 'all'),('subject', 'subject'),('staff', 'staff'), ('semester', 'semester'), ]
    choices_list = [('all', 'all'),('id', 'id'), ('subject_id', 'subject_id'), ('semester', 'semester'), ]
    # ('first name', 'first name'), ('last name', 'last name'),

    filter_by = forms.ChoiceField(label="Filter by ", choices=choices_list1, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", ' hx-target': "#get_by", 'hx-swap': 'outerHtml', 'hx-post': "filter-by", 'hx-trigger': "change"}), required=True, help_text='Select filter type on or allow the default as all', initial=choices_list1[0])
    

    get_by = forms.ChoiceField(label="Get By", choices=[], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1 get_by ", ' hx-target': "#tableContent", 'hx-post': "filter-attendance", 'hx-trigger': "change"}), required=False, help_text='Select the data category or allow the default as all', initial=choices_list1[0])
    
    # class_room = forms.ChoiceField(label="Class", choices=classes, widget=forms.Select(
    #     attrs={'class': "form-control rounded", 'id': "exampleInputEmail1 ", ' hx-target': "#tableContent", 'hx-post': "filter-attendance", 'hx-trigger': "change"}), required=True, help_text='Select the data category of a specific class or allow the default as all')

    sort_by = forms.ChoiceField(label="sort by", choices=choices_list, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1 sort_by", ' hx-target': "#tableContent", 'hx-post': "filter-attendance", 'hx-trigger': "change"}), required=True, help_text='Select a filter by option to continue the filtering or allow the default as all', initial=choices_list[0])
 

class StudentMarksFilterForm(forms.Form):

    classes = [('all', 'all'), ]
    try:
        
        for class_r in ClassRoom.objects.all():
            classes.append((class_r.name, class_r.name))
    except :
        pass


    choices_list1 = [('all', 'all'), ('subject', 'subject'),('staff', 'staff'), ('semester', 'semester'), ]
    
    choices_list = [('all', 'all'),('id', 'id'),('staff_id', 'staff_id'),('subject_id', 'subject_id'),  ('semester', 'semester'), ]
    # ('first name', 'first name'), ('last name', 'last name'),

    filter_by = forms.ChoiceField(label="Filter by ", choices=choices_list1, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", ' hx-target': "#get_by", 'hx-swap': 'outerHtml', 'hx-post': "student-filter-by", 'hx-trigger': "change"}), required=True, help_text='Select filter type on or allow the default as all', initial=choices_list1[0])
    

    get_by = forms.ChoiceField(label="Get By", choices=[], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", ' hx-target': "#tableContent", 'hx-post': "filter-marks", 'hx-trigger': "change"}), required=False, help_text='Select the data category or allow the default as all', initial=choices_list1[0])
    
    

    sort_by = forms.ChoiceField(label="sort by", choices=choices_list, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1 sort_by", ' hx-target': "#tableContent", 'hx-post': "filter-marks", 'hx-trigger': "change"}), required=True, help_text='Select a filter by option to continue the filtering or allow the default as all', initial=choices_list[0])
 
choices = [('Mr', 'Mr'), ('Mrs', 'Mrs'), ("Sir","Sir"), ('Prof','Prof'),
           ('Miss', 'Miss'), ('Misses', 'Misses'), ('Doctor', 'chief'), ('senator', "senator")]

class StudentAdmissionForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter first name')

    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter middle and last name')

    email = forms.EmailField(label="Email Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Enter User valid email address')

    address = forms.CharField(label="Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter home address')

    place_of_birth = forms.CharField(label="Place Of Birth", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter Place of bith')

    gender = forms.ChoiceField(label="Gender", choices=[('M', 'Male'), ('F', 'Female'), ('0', "Others")], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select gender')
    
    user_type = forms.ChoiceField(label="User type", choices=[ ('3', "Student")], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select user type', initial=("3", "Student"))

    phone = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={
                            'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter a working phone number')

    date_of_birth = forms.DateField(widget=forms.DateInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", 'type': "date"}), help_text="Enter the date of birth of student FORMAT: YEAR-MONTH-DAY")

    class_room = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), label="Class", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select class of student ")

    department = forms.ModelChoiceField(queryset=Department.objects.all(), label="Department", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select department of student ")
   
    profile_picture = forms.ImageField(label="Profile Picture", widget=forms.FileInput(attrs={'class': "custom-file-input", 'id': "exampleInputFile"}))
    
    guardian_profile_picture = forms.ImageField(label=" Guardian Profile Picture", required=False, widget=forms.FileInput(attrs={'class': "custom-file-input", 'id': "exampleInputFile"}))
    
    guardian_title = forms.ChoiceField(label="Title", choices=choices, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select title')
    guardian_full_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter full name')

    guardian_email = forms.EmailField(label="Email Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Enter User valid email address')

    guardian_address = forms.CharField(label="Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter home address')
    guardian_phone = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={
                            'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter a working phone number')

    class Meta:
        model = Admission
        fields = '__all__'


class StudentGovernmentForm(forms.ModelForm):
    
    """Form definition for StudentGovernment."""
    student_id = forms.ModelChoiceField(queryset=Student.objects.all(), label="Student name", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select who to Student")
    
    position = forms.CharField(label="position ", widget=forms.TextInput(attrs={
                            'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter  position ')


    class Meta:
        """Meta definition for StudentGovernmentform."""

        model = StudentGovernment
        fields = "__all__"
