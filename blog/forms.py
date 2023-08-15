from django import forms
# from ckeditor.fields import ( CKEditorWidget,RichTextFormField )
from blog.models import Blogpost, Comment


class BlogpostForm(forms.ModelForm):
    # title = forms.CharField(widget=forms.TextInput(
    #     attrs={'placeholder': 'title', 'class': 'form-control'}))
    # content = forms.CharField(widget=CKEditorWidget(
    #     attrs={'placeholder': ' post  content here', 'class': 'form-control',}))
    # pub_date = forms.DateTimeField(label='published date:', widget=forms.DateTimeInput(
    #     attrs={'placeholder': ' enter date in this formate:year-month-day (2020-05-03)', 'class': 'form-control vDateField', 'type': 'date'}))

    class Meta:
        model = Blogpost
        fields = ['content']


class CommentForm(forms.ModelForm):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'type your comment here', 'class': 'form-control', 'columns': 4, 'rows': 2}))

    class Meta:
        model = Comment
        fields = ['text']
