from django.contrib.auth.models import User
from django import forms
from .models import School, Register


class LoginForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['email', 'password']

class RequestpwdForm(forms.ModelForm):
	email = forms.CharField(widget=forms.EmailInput)

	class Meta:
		model = User
		fields = ['email']

class RegistrationForm(forms.ModelForm):
	email = forms.CharField(widget=forms.EmailInput)
	password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = Register
		fields = [ "first_name", "last_name", "email", "password", "confirm_password","is_school_registered"]

class SchoolForm(forms.ModelForm):
	class Meta:
		model = School
		fields = [ "school_name", "school_address_line_1", "line_2", "city", "district", "state"]