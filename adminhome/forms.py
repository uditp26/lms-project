from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import School, Student, Teacher, Principal
from phonenumber_field.formfields import PhoneNumberField

class RegisterschoolForm(forms.ModelForm):
    school_name = forms.CharField(max_length=500)
    class_upto = forms.IntegerField()
    address = forms.Textarea()
    city = forms.CharField(max_length = 50)
    district = forms.CharField(max_length = 50)
    state = forms.CharField(max_length = 50)
    # filling address fields based on pincode
    pincode = forms.IntegerField()

    class Meta:
        model = School
        fields = ['school_name', 'class_upto', 'address', 'city', 'district', 'state', 'pincode']

class AddstudentForm(forms.ModelForm):
    first_name = forms.TextInput()
    last_name = forms.TextInput()
    date_of_birth = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    admission_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    email = forms.EmailInput()
    address = forms.Textarea()
    study = forms.NumberInput()

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'date_of_birth', 'admission_date', 'email', 'address', 'study']

class AddteacherForm(forms.ModelForm):
    first_name = forms.TextInput()
    last_name = forms.TextInput()
    date_of_birth = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    joining_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    email = forms.EmailInput()
    address = forms.Textarea()
    phone = PhoneNumberField(widget=forms.TextInput(), required=False)
    is_class_teacher = forms.BooleanField(required=False)
    class_teacher_of = forms.NumberInput()
    subject = forms.TextInput()
    resume = forms.FileField()

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'date_of_birth', 'joining_date', 'email', 'address', 'phone', 'is_class_teacher', 'class_teacher_of', 'subject', 'resume']

class AddprincipalForm(forms.ModelForm):
    first_name = forms.TextInput()
    last_name = forms.TextInput()
    date_of_birth = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    joining_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    email = forms.EmailInput()
    address = forms.Textarea()
    phone = PhoneNumberField(widget=forms.TextInput(), required=False)
    is_teacher = forms.BooleanField(required=False)
    subject = forms.CharField(required=False)
    resume = forms.FileField()

    class Meta:
        model = Principal
        fields = ['first_name', 'last_name', 'date_of_birth', 'joining_date', 'email', 'address', 'phone', 'is_teacher', 'subject', 'resume']
