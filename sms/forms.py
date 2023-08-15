from django import forms
from fees.models import Fee

from student.models import ClassRoom, Student

semesters=[('ft',"first Trimester"),('st','second Trimester'),('tt','third Trimester')]
class FeeForm(forms.Form):
    semesters = [('ft', "First Trimester"), ("st", "Second Trimester"),
                 ("tt", "Third Trimester")]
    entries = [('select student entry type', 'select student entry type'),("N", "New"), ("O", "Old")]
    """Form definition for Fee."""
    student_id = forms.ModelChoiceField(queryset=Student.objects.all(), label="Student name", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select student name")
    class_room = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), label="Class", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select class of student ")
     
    entry = forms.ChoiceField(label="Entry", choices=entries, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", 'hx-post': "check_fee_student_type", 'hx-trigger': "change", 'hx-target': '#new'}), required=True, help_text='Select student entry to indicate if student is new or old student', initial=entries[0])  
    
    
    semester = forms.ChoiceField(label="Trimester", choices=semesters, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select select trimester in which school fees was paid')

    amount = forms.FloatField(label="Amount ", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1 ", 'hx-post': "fee-check-remaining", 'hx-trigger': "keyup change delay: 2s ", 'hx-target': '#new'}), required=True, help_text='Enter the amount of money to pay now')
    
    amount_in_words = forms.CharField( widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Enter the paid amount in words ')
    phone = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={
                            'class': "form-control rounded", 'id': "exampleInputEmail1"}),  max_length=100, required=True, help_text='Enter Your MTN Mobile Money Number Here ie the number you want to do the payment with')

    # class Meta:
    #     """Meta definition for Feeform."""

    #     model = Fee
    #     fields = ('student_id',"class_room",'entry','semester','amount','amount_in_words',)


class GetStudentForm(forms.Form):
    class_room = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), label="Class", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select class of student ")
    
    
    
    
    
    
class certificateFilterForm(forms.Form):
    class_id = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), label="Class", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select class")
    
   
    semester = forms.ChoiceField(label="Trimester", choices=semesters, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select select semester in which certificate is to be recorded')
    