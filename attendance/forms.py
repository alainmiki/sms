# Django Libs:
from django import forms

from student.models import AttendanceReport, Subject
from student.models import ClassRoom


semesters=[('ft',"first trimester"),('st','second trimester'),('tt','third trimester')]

class SubjectForm(forms.ModelForm):
    """Form definition for Subject."""
    name = forms.CharField(label="Subject Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=100, required=True, help_text='Enter the name of a subject ')


    coefficient = forms.IntegerField(label="Subject Coefficients ", widget=forms.NumberInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Enter the coefficients of the subject',initial=3)

    class Meta:
        """Meta definition for Subjectform."""

        model = Subject
        fields='__all__'


class AttendanceReportForm(forms.ModelForm):
    """Form definition for AttendanceReport."""

    class Meta:
        """Meta definition for AttendanceReportform."""

        model = AttendanceReport
        fields = '__all__'

class AttendanceFilterForm(forms.Form):
    class_id = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), label="Class", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select class to take attendance")
    
    subject_id = forms.ModelChoiceField(queryset=Subject.objects.all(), label="Subject", widget=forms.Select(
        attrs={"class": "form-control"}), help_text="Select subject to take attendance")

    semester = forms.ChoiceField(label="Semester", choices=semesters, widget=forms.Select(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True, help_text='Select the semester in which the attendance is taken ')