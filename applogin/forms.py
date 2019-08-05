from django.contrib.auth.models import User
from django import forms


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

class ResetpwdForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['password', 'confirm_password']
