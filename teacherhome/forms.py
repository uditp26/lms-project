from django.contrib.auth.models import User
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from adminhome.models import Teacher 
from .models import Assignment, ClassAttendance, SendMessage, SendResult

class AddassignForm(forms.ModelForm):
    class_number = forms.IntegerField()
    subject = forms.CharField(max_length = 20)
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    due_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    assignement_file = forms.FileField()

    class Meta:
        model = Assignment
        fields = ['class_number', 'subject', 'start_date', 'due_date', 'assignement_file']

class ClassAttendanceForm(forms.ModelForm):
    roll_number = forms.CharField(max_length = 20)
    name = forms.CharField(max_length = 30)
    is_present = forms.CharField(max_length = 1)
    class Meta:
        model = ClassAttendance
        fields = ['roll_number', 'is_present']
        
class SendMessageForm(forms.ModelForm):
    roll_number = forms.CharField(max_length = 50)
    email_id = forms.CharField(widget=forms.EmailInput)
    report_message = forms.Textarea()
    class Meta:
        model = SendMessage
        fields = ['roll_number', 'email_id', 'report_message']

class SendResultForm(forms.ModelForm):
    roll_number = forms.CharField(max_length = 50)
    email_id = forms.CharField(widget=forms.EmailInput)
    result = forms.FileField()
    class Meta:
        model = SendResult
        fields = ['roll_number', 'email_id', 'result']

class updateteacherForm(forms.ModelForm):
    first_name = forms.TextInput()
    last_name = forms.TextInput()
    date_of_birth = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    joining_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    email = forms.EmailInput()
    phone = PhoneNumberField(widget=forms.TextInput(), required=False)
    is_class_teacher = forms.BooleanField(required=False)
    subject = forms.TextInput()
    resume = forms.FileField()

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'date_of_birth', 'joining_date', 'email', 'phone', 'is_class_teacher', 'subject', 'resume']