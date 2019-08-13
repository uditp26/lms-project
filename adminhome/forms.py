from django.contrib.auth.models import User
from django import forms
from .models import School, Student, Teacher

class RegisterschoolForm(forms.ModelForm):
    school_name = forms.CharField(max_length=500)
    address = forms.Textarea()
    city = forms.CharField(max_length = 50)
    district = forms.CharField(max_length = 50)
    state = forms.CharField(max_length = 50)
    # filling address fields based on pincode
    pincode = forms.IntegerField()

    class Meta:
        model = School
        fields = ['school_name', 'address', 'city', 'district', 'state', 'pincode']

class AddstudentForm(forms.ModelForm):
    first_name = forms.TextInput()
    last_name = forms.TextInput()
    date_of_birth = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    admission_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    email = forms.EmailInput()
    study = forms.NumberInput()

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'date_of_birth', 'admission_date', 'email', 'study']

class AddteacherForm(forms.ModelForm):
    first_name = forms.TextInput()
    last_name = forms.TextInput()
    date_of_birth = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    joining_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    email = forms.EmailInput()
    phone = forms.NumberInput()
    is_class_teacher = forms.BooleanField(required=False)
    resume = forms.FileField()

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'date_of_birth', 'joining_date', 'email', 'phone', 'is_class_teacher', 'resume']
