
from django import forms


from django import forms

from adminhod.models import CustomUser
from student.models import Subject
from library.models import Assignment, Library
from student.models import ClassRoom
from .models import LeaveReportStaff, Staff



from django.contrib.auth.forms import UserCreationForm

class StaffRegistrationForm(UserCreationForm):
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
    user_type = forms.ChoiceField(label="User type", choices=[('2', 'Sfaff')], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select user type', initial=('2', 'Sfaff'))

    phone = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={
                            'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter a working phone number')

    duty_post = forms.CharField(
        label="Duty Post", widget=forms.TextInput(attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter where the staff will be or is assigned to')

    matricule = forms.CharField(label="Matriculate ", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter staff matriculate Number ')

    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), widget=forms.SelectMultiple(
        attrs={'multiple': 'true', 'class': "form-control rounded", 'id': "exampleInputEmail1 id_subjects"},), help_text='Select the subjects that the staff teaches Hold CTR+MOUSE LEFT CLICK to select multiple subjects', )

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1",'hidden':'true'}), max_length=100,disabled=True,show_hidden_initial=False, required=False, help_text='Enter a valid secure password it should be more than 6 characters')

    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1",'hidden':'true'}), max_length=100,disabled=True,show_hidden_initial=False, required=False, help_text='Enter enter the previous password make sure it matches')
    
    profile_picture = forms.ImageField(label="Profile Picture", widget=forms.FileInput(attrs={'class': "custom-file-input", 'id': "exampleInputFile"}))

    class Meta:
        model=CustomUser
        fields = ['first_name', 'last_name', 'email', 'address', 'gender',
                  'place_of_birth', 'phone', 'user_type', 'profile_picture']

class GenerallStaffNotificationForm(forms.Form):
    sender_name = forms.CharField(label="Sender's Name", widget=forms.TextInput(
       attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter the name of the person sending this notification or the person who ordered the sending ')

    
    message=forms.CharField(label="Massage",widget=forms.Textarea(attrs={'col':12,'row':12,"class":"form-control"}), required=True,help_text='write the information to send')

class SpecificStaffNotificationForm(forms.Form):
    sender_name = forms.CharField(label="Sender's Name", widget=forms.TextInput(
       attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter the name of the person sending this notification or the person who ordered the sending ')

    
    staff = forms.ModelChoiceField(queryset=Staff.objects.all(),label="Staff to noty", widget=forms.Select(attrs={"class":"form-control"}),help_text="Select who to send notification")
    
    message=forms.CharField(label="Massage",widget=forms.Textarea(attrs={'col':12,'row':12,"class":"form-control"}), required=True,help_text='write the information to send')
        
    
    
class StaffForm(forms.Form):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'class':"form-control rounded",'id':"exampleInputEmail1"}), max_length=100, required=True,help_text='Enter first name')
    
    
    last_name=forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'class':"form-control rounded",'id':"exampleInputEmail1"}), max_length=100, required=True,help_text='Enter middle and last name')
    
    email = forms.EmailField(label="Email Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True,help_text='Enter User valid email address')
    
    address = forms.CharField(label="Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter home address')
    gender = forms.ChoiceField(label="Gender", choices=[('M','Male'), ('F','Female'), ('0',"Others")], widget=forms.Select(attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),required=True, help_text='Select gender')

    phone = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={
                            'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter a working phone number')

    
    duty_post = forms.CharField(
        label="Duty Post", widget=forms.TextInput(attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter where the staff will be or is assigned to')
    
    matricule = forms.CharField(label="Matriculate ", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True,help_text='Enter staff matriculate Number ')
    
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), widget=forms.SelectMultiple(
        attrs={'multiple': 'true', 'class': "form-control rounded", 'id': "exampleInputEmail1 id_subjects"},), help_text='Select the subjects that the staff teaches Hold CTR+MOUSE LEFT CLICK to select multiple subjects', )

    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter a valid secure password it should be more than 6 characters')
    
    repeat_password = forms.CharField(label="Repeat Password", widget=forms.PasswordInput(attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter enter the previous password make sure it matches')
    profile_picture = forms.ImageField(label="Profile Picture", widget=forms.FileInput(attrs={'class': "custom-file-input",
                    'id':"exampleInputFile"}))
    
 
class StaffUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter first name')

    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter middle and last name')
    username = forms.CharField(label="Username", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter username it should be first + last name')


    email = forms.EmailField(label="Email Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Enter User valid email address')

    address = forms.CharField(label="Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter home address')
    
    place_of_birth = forms.CharField(label="Place Of Birth", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter Place of bith')
    
    gender = forms.ChoiceField(label="Gender", choices=[('M', 'Male'), ('F', 'Female'), ('0', "Others")], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select gender')
    user_type = forms.ChoiceField(label="User type", choices=[('1', 'HOD'), ('2', 'Sfaff'), ('3', "Student"),("4","Guardian")], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select user type',initial=(('2',"Staff")))

    phone = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={
                            'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter a working phone number')

    duty_post = forms.CharField(
        label="Duty Post", widget=forms.TextInput(attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter where the staff will be or is assigned to')

    matricule = forms.CharField(label="Matriculate ", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter staff matriculate Number ')

    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), widget=forms.SelectMultiple(
        attrs={'multiple': 'true', 'class': "form-control rounded", 'id': "exampleInputEmail1 id_subjects"},), help_text='Select the subjects that the staff teaches Hold CTR+MOUSE LEFT CLICK to select multiple subjects', )

    class Meta:
        """Meta definition for StaffLeaveFormform."""

        model=CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'address', 'gender',
                    'place_of_birth', 'phone',  'user_type']

class StaffLeaveFormForm(forms.ModelForm):
    """Form definition for StaffLeaveForm."""
    # staff_id = forms.ModelChoiceField(queryset=Staff.objects.all(),label="Staff name", widget=forms.Select(attrs={"class":"form-control"}),help_text="Select who to apply leave",required=False)
    
    leave_start_date = forms.DateTimeField(widget=forms.DateInput(attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", 'type': "date"}), help_text="Enter the date and time your leave will will start")
    
    leave_end_date=forms.DateTimeField(widget=forms.DateInput(attrs={'class': "form-control rounded", 'id': "exampleInputEmail1",'type':"date"
        
    }),help_text="Enter the date and time your leave will expire")
    
    leave_message = forms.CharField(widget=forms.Textarea(
        attrs={'col': 12, 'row': 12, "class": "form-control"}), required=True, help_text='write the information to send')
    
    class Meta:
        """Meta definition for StaffLeaveFormform."""

        model = LeaveReportStaff
        fields = ('leave_start_date', 'leave_end_date', 'leave_message',)


class AssignmentForm(forms.ModelForm):
    """Form definition for Assignment."""
    class_room = forms.ModelMultipleChoiceField(queryset=ClassRoom.objects.all(), widget=forms.SelectMultiple(
        attrs={'multiple': 'true', 'class': "form-control rounded", 'id': "exampleInputEmail1 id_subjects"},), help_text='Select the classes that the assignment is been assign too CTR+MOUSE LEFT CLICK to select multiple classes', )
        
    submission_date = forms.DateField(widget=forms.DateInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", 'type': "date"}), help_text="Enter the date in which the assignment will be submitted ")
        
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select the subject  ")


    class Meta:
        """Meta definition for Assignmentform."""
       

        model = Assignment
        fields = ['class_room','subject','submission_date','content']



class AttendanceFilterForm(forms.Form):



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
 
