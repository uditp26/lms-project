from django.contrib.auth.models import User
from django import forms
from .models import Assignment, ClassAttendance, SendMessage, SendResult

class AddassignForm(forms.ModelForm):
    class_number = forms.TextInput()
    subject = forms.TextInput()
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    due_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    assignement_file = forms.FileField()

    class Meta:
        model = Assignment
        fields = ['class_number', 'subject', 'start_date', 'due_date', 'assignement_file']

class ClassAttendanceForm(forms.ModelForm):
    roll_number = forms.TextInput()
    is_present = forms.TextInput()
    class Meta:
        model = ClassAttendance
        fields = ['roll_number', 'is_present']
        
class SendMessageForm(forms.ModelForm):
    roll_number = forms.TextInput()
    email_id = forms.CharField(widget=forms.EmailInput)
    report_message = forms.TextInput()
    class Meta:
        model = SendMessage
        fields = ['roll_number', 'email_id', 'report_message']

class SendResultForm(forms.ModelForm):
    roll_number = forms.TextInput()
    email_id = forms.CharField(widget=forms.EmailInput)
    result = forms.FileField()
    class Meta:
        model = SendResult
        fields = ['roll_number', 'email_id', 'result']
