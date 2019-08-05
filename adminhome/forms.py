from django.contrib.auth.models import User
from django import forms

class AddstudentForm(forms.ModelForm):
    first_name = forms.TextInput()
    last_name = forms.TextInput()
    email = forms.EmailInput()
    admission_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'admission_date']

class AddteacherForm(forms.ModelForm):
    first_name = forms.TextInput()
    last_name = forms.TextInput()
    email = forms.EmailInput()
    joining_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    is_class_teacher = forms.BooleanField(required=False)
    resume = forms.FileField()


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'joining_date', 'is_class_teacher', 'resume']