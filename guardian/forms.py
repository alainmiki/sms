
from django import forms
from adminhod.models import CustomUser

# from guardian.models import Guardian
from student.models import Student,Guardian
choices = [('Mr', 'Mr'), ('Mrs', 'Mrs'), ("Sir","Sir"), ('Prof','Prof'),
           ('Miss', 'Miss'), ('Misses', 'Misses'), ('Doctor', 'chief'), ('senator', "senator")]

class GuardianRegForm(forms.ModelForm):
    
  
    title = forms.ChoiceField(label="Title", choices=choices, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select title')
    
    children = forms.ModelMultipleChoiceField(queryset=Student.objects.all(), widget=forms.SelectMultiple(
        attrs={'multiple': 'true', 'class': "form-control rounded", 'id': "exampleInputEmail1 id_Students",'required':'false'},), help_text='Select the Students that belongs to the gurdian Hold CTR+MOUSE LEFT CLICK to select multiple Students' )

    first_name = forms.CharField(label="First Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter first name')

    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter middle and last name')

    email = forms.EmailField(label="Email Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Enter User valid email address')

    address = forms.CharField(label="Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter home address')


    gender = forms.ChoiceField(label="Gender", choices=[('M', 'Male'), ('F', 'Female'), ('0', "Others")], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select gender')
   
    user_type = forms.ChoiceField(label="User type", choices=[('4', 'Guardian')], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select user department type', initial=('4', 'Guardian'))
   
    phone = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={
                            'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter a working phone number')


   
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1",'hidden':'true'}), max_length=100,disabled=True,show_hidden_initial=False, required=False, help_text='Enter a valid secure password it should be more than 6 characters')

    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1",'hidden':'true'}), max_length=100,disabled=True,show_hidden_initial=False, required=False, help_text='Enter enter the previous password make sure it matches')
    
    profile_picture = forms.ImageField(label="Profile Picture",required=False, widget=forms.FileInput(attrs={'class': "custom-file-input",'id': "exampleInputFile"}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'address', 'gender',
                 'phone','password1','password2', 'user_type', 'profile_picture']


class GuardianUpdateForm(forms.ModelForm):
    
  
    title = forms.ChoiceField(label="Title", choices=choices, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select title')
    
    children = forms.ModelMultipleChoiceField(queryset=Student.objects.all(),required=False, widget=forms.SelectMultiple(
        attrs={'multiple': 'true', 'class': "form-control rounded", 'id': "exampleInputEmail1 id_Students",'required':'false'},), help_text='Select the Students that belongs to the gurdian Hold CTR+MOUSE LEFT CLICK to select multiple Students' )

    first_name = forms.CharField(label="First Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter first name')

    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter middle and last name')

    email = forms.EmailField(label="Email Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Enter User valid email address')

    address = forms.CharField(label="Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter home address')


    gender = forms.ChoiceField(label="Gender", choices=[('M', 'Male'), ('F', 'Female'), ('0', "Others")], widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select gender')
   
   
    phone = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={
                            'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter a working phone number')


    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'address', 'gender',
                 'phone',]





class GeneralGuardianNotificationForm(forms.Form):
    sender_name = forms.CharField(label="Sender's Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter the name of the person sending this notification or the person who ordered the sending ')
    message = forms.CharField(label="Massage", widget=forms.Textarea(
        attrs={'col': 12, 'row': 12, "class": "form-control"}), required=True, help_text='write the information to send')


class SpecificGuardianNotificationForm(forms.Form):
    sender_name = forms.CharField(label="Sender's Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter the name of the person sending this notification or the person who ordered the sending ')

    guardian_id = forms.ModelChoiceField(queryset=Guardian.objects.all(), label="Guardian to notify", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select who to send notification")

    message = forms.CharField(label="Massage", widget=forms.Textarea(
        attrs={'col': 12, 'row': 12, "class": "form-control"}), required=True, help_text='write the information to send')

