from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'password']

class RegistrationForm(UserCreationForm):
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)
	email = forms.CharField(widget=forms.EmailInput)
	username = forms.CharField(max_length=50)

	class Meta:
		model = User
		fields = [ "first_name", "last_name", "email", "username"]

class RequestpwdForm(forms.ModelForm):
	email = forms.CharField(widget=forms.EmailInput)

	class Meta:
		model = User
		fields = ['email']

class ResetpwdForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(widget=forms.PasswordInput)
	password_confirmation = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'password', 'password_confirmation']
