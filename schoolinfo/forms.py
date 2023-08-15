
from django import forms
from schoolinfo.models import Activity, SchoolInformation




class ActivityForm(forms.ModelForm):
    """Form definition for Activity."""
     
    name = forms.CharField(widget=forms.TextInput(
    attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True)
    description = forms.CharField(widget=forms.Textarea(
    attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), required=True)
    
    class Meta:
        """Meta definition for Activityform."""
       

        model = Activity
        fields = "__all__"




class SchoolInformationForm(forms.ModelForm):
    """Form definition for SchoolInformation."""
    
    school_name_abbreviation = forms.CharField(label="School Name Abbreviation", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True, help_text='Enter the name of the school in short ')
    
    
    
    school_name_full = forms.CharField(label="School Full Name", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True, help_text='Enter the name of the school in full')
    
    address = forms.CharField(label="Location / Address", widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True)
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True)
    
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True)
    
    fee_phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True)
    
    whatsApp = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True)
    
    website = forms.CharField(widget=forms.URLInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True)
    
    new_student_fee = forms.CharField(widget=forms.NumberInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True)
    
    old_student_fee = forms.CharField(widget=forms.NumberInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True)
    
    
    motto = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True)
    
    
    region = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True)
    
    town = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True)
    
    po_box = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control rounded", 'id': "exampleInputEmail1"}), max_length=250, required=True)
    
    school_logo = forms.ImageField(label="School Logo", widget=forms.FileInput(attrs={'class': "custom-file-input",'id': "exampleInputFile",'onchange':'getiImg2Display(event)'}),required=False)
    
    h_o_s_signature = forms.ImageField(label="Head of School Signature", widget=forms.FileInput(attrs={'class': "custom-file-input",'id': "exampleInputFile",'onchange':'getiImg2Display(event)'}),required=False)
    
    school_stamp = forms.ImageField(label="School Stamp", widget=forms.FileInput(attrs={'class': "custom-file-input",'id': "exampleInputFile",'onchange':'getiImg2Display(event)'}),required=False)
    
    school_banner_image = forms.ImageField(label="school Banner Image", widget=forms.FileInput(attrs={'class': "custom-file-input",'id': "exampleInputFile",'onchange':'getiImg2Display(event)'}),required=False)
    


    class Meta:
        """Meta definition for SchoolInformationform."""

        model = SchoolInformation
        fields = '__all__'
