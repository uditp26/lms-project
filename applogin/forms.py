from django.contrib.auth.models import User
from django import forms
from .models import School, Register


class LoginForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'password']

class RequestpwdForm(forms.ModelForm):
	email = forms.CharField(widget=forms.EmailInput)

	class Meta:
		model = User
		fields = ['email']

class RegistrationForm(forms.ModelForm):
	email = forms.CharField(widget=forms.EmailInput)
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = [ "username", "email", "password"]

class SchoolForm(forms.ModelForm):
	class Meta:
		model = School
		fields = [ "school_name", "school_address_line_1", "line_2", "city", "district", "state"]