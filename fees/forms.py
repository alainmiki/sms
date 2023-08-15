# Django Libs:
from random import choices
from django import forms

from fees.models import Fee
from student.models import ClassRoom, Student

			
class FeeForm(forms.ModelForm):
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
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select select Trimester in which school fees was paid')

    amount = forms.FloatField(label="Amount ", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1 ", 'hx-post': "fee-check-remaining", 'hx-trigger': "keyup change delay: 2s ", 'hx-target': '#new'}), required=True, help_text='Enter the amount of money to pay now')
    
    amount_in_words = forms.CharField( widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Enter the paid amount in words ')

    class Meta:
        """Meta definition for Feeform."""

        model = Fee
        fields = ('student_id',"class_room",'entry','semester','amount','amount_in_words',)

class FilterForm(forms.Form):
    
    classes=[('all','all'),]
    try:
        
        for class_r in ClassRoom.objects.all():
            classes.append((class_r.name, class_r.name))
    except :
        pass
    
    choices_list = [('all', 'all'), ('class_room', 'class_room'),
               ('partly_paid', 'partly_paid'), ('fully_paid', 'fully_paid'), ] 
    
    choices_list1 = [('all', 'all'),('partly_paid', 'partly_paid'), ('fully_paid', 'fully_paid'), ] 
    # ('first name', 'first name'), ('last name', 'last name'),
   
    class_room = forms.ChoiceField(label="Filter by Class", choices=classes, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", ' hx-target': "#tableContent", 'hx-post': "fees-filter", 'hx-trigger': "change"}), required=True, help_text='Select class to filter on or allow the default as all', initial=classes[0])
    
    get_by = forms.ChoiceField(label="Get By", choices=choices_list1, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", ' hx-target': "#tableContent", 'hx-post': "fees-filter", 'hx-trigger': "change"}), required=True, help_text='Select the data category or allow the default as all', initial=choices_list1[0])
    
    filter_by = forms.ChoiceField(label="sorted by", choices=choices_list, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1", ' hx-target': "#tableContent", 'hx-post': "fees-filter", 'hx-trigger': "change"}), required=True, help_text='Select a filter by option to continue the filtering or allow the default as all', initial=choices_list[0])
