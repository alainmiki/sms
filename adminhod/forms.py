
from django import forms
from django.forms import (ModelForm, inlineformset_factory)
from student.models import Subject
from library.models import DocumentOfStaff, Library, Pass_Question

from student.models import ClassRoom

from .models import AdminHOD, CustomUser,Event, Gallery

user_department_data = (('1', "admin"), ('2', "secretary"),
                        ('3', 'bossier'), ('4', 'chief of staff'))


class EventForm(forms.ModelForm):
    """Form definition for Event."""
    
    title = forms.CharField(label="Title", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True, help_text='Enter the title of the event')
    
    location = forms.CharField(label="Location", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True, help_text='enter the venue of the event ')
    
    start_date_and_time = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", 'type': "datetime-local"}), help_text="Enter the date and time that the event will start",input_formats=['mm/dd/yyyy hh:mm'])

    end_date_and_time = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", 'type': "datetime-local"}), help_text="Enter the date and time that the event will end", input_formats=['mm/dd/yyyy [hh:mm'])

    
    description = forms.CharField(label="Description", widget=forms.Textarea(
        attrs={'col': 12, 'row': 12, "class": "form-control"}), required=True, help_text='Describe  this event in good words manner')

    class Meta:
        """Meta definition for Eventform."""

        model = Event
        fields = "__all__"


class GalleryForm(forms.ModelForm):
    categories = [('student', 'student'), ('staff', 'staff'),
                  ('adminhod', 'adminhod'), ('guardian', "guardian")]
    """Form definition for Gallery."""
    
    category = forms.ChoiceField(label="Category", choices=categories, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select image category',)
    
    image = forms.ImageField(label="Image", widget=forms.FileInput(attrs={'class': "custom-file-input",'id': "exampleInputFile",'onchange':'getiImg2Display(event)'}))


    class Meta:
        """Meta definition for Galleryform."""

        model = Gallery
        fields = '__all__'


class AdminHODForm(forms.ModelForm):
  
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
   
    user_type = forms.ChoiceField(label="User type", choices=[('1', 'HOD')], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select user department type', initial=('1', 'HOD'))
    
    user_department = forms.ChoiceField(label="User department", choices=user_department_data, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select user type', initial=user_department_data[0])

    phone = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={
                            'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter a working phone number')

    post = forms.CharField(
        label="Post", widget=forms.TextInput(attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter where the staff will be or is assigned to')

   
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1",'hidden':'true'}), max_length=100,disabled=True,show_hidden_initial=False, required=False, help_text='Enter a valid secure password it should be more than 6 characters')

    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1",'hidden':'true'}), max_length=100,disabled=True,show_hidden_initial=False, required=False, help_text='Enter enter the previous password make sure it matches')
    
    profile_picture = forms.ImageField(label="Profile Picture", widget=forms.FileInput(attrs={'class': "custom-file-input",'id': "exampleInputFile"}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'address', 'gender',
                  'place_of_birth', 'phone','password1','password2', 'user_type', 'profile_picture']
   


class AdminHODUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter first name')

    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter middle and last name')
    
    email = forms.EmailField(label="Email Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Enter User valid email address')

    address = forms.CharField(label="Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter home address')

    place_of_birth = forms.CharField(label="Place Of Birth", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter Place of birth')

    gender = forms.ChoiceField(label="Gender", choices=[('M', 'Male'), ('F', 'Female'), ('0', "Others")], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select gender')
    
    user_type = forms.ChoiceField(label="User type", choices=[('1', 'HOD'), ], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select user type', initial=(('1', 'HOD')))
    
    user_department = forms.ChoiceField(label="User department", choices=user_department_data, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select user type', initial=user_department_data[0])

    phone = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={
                            'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter a working phone number')

    post = forms.CharField(
        label="Post", widget=forms.TextInput(attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter where the staff will be or is assigned to')
    class Meta:
        """Meta definition for StaffLeaveFormform."""

        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'address', 'gender',
                  'place_of_birth', 'phone',  'user_type']


class LibraryForm(forms.ModelForm):
   
    

    title=forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter Book Title')
    
    author=forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter Author names')    
    poster=forms.ImageField(label="Poster", widget=forms.FileInput(attrs={'class': "custom-file-input",'id': "exampleInputFile"}))

    subject=forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select the subject  ")
    
    book=forms.FileField(label="Book", widget=forms.FileInput(attrs={'class': "custom-file-input",'id': "exampleInputFile"}))


    class Meta:

        model = Library
        fields ="__all__"

class Pass_QuestionForm(forms.ModelForm):
   
    

    title=forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter paper Title')
    
   
    subject=forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select the subject  ")
    
    paper=forms.FileField(label="paper", widget=forms.FileInput(attrs={'class': "custom-file-input",'id': "exampleInputFile"}))


    class Meta:

        model = Pass_Question
        fields ="__all__"


class DocumentOfStaffForm(forms.ModelForm):
   
    

    title=forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter document Title')
    
    author=forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter Author names')    
    poster=forms.ImageField(label="Poster", widget=forms.FileInput(attrs={'class': "custom-file-input",'id': "exampleInputFile"}))
    subject=forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select the subject  ")
    
    document=forms.FileField(label="Document", widget=forms.FileInput(attrs={'class': "custom-file-input",'id': "exampleInputFile"}))


    class Meta:

        model = DocumentOfStaff
        fields ="__all__"

AdminHODFormset = inlineformset_factory(
    CustomUser, AdminHOD, AdminHODForm, can_delete=False, min_num=2, extra=4
)
