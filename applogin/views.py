from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RequestpwdForm, RegistrationForm, SchoolForm
from django.views import generic

from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import School, Register
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password


class LoginFormView(View):
    form_class = LoginForm
    template_name = 'applogin/login_form.html'

    # displays a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
                                   
    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        #determine which radio button is selected
        radio_btn = request.POST.get('radio_btn')
        print("selected button number =", radio_btn)

        if form.is_valid():

            user = form.save(commit = False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']    
            user.set_password(password)
            user.save()
            # reg =  Register()
            # it will return users objects if credentials are correct  
            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    
                    return redirect('applogin:registerschool')
        return render(request, 'applogin/login_form.html', {'form': form})


class RegistrationFormView(View):
    form_class = RegistrationForm
    template_name = 'applogin/registration_form.html'
    
    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #put data inside blank text fields 
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']    
            user.set_password(password)
            user.save()     
            # it will return users objects if credentials are correct  
        return render(request, 'applogin/login_form.html', {'form': form})

class SchoolFormView(View):
    form_class = SchoolForm
    template_name = 'applogin/school_form.html'
    
    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #put data inside blank text fields
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            school_obj = form.save(commit = False)
            school_obj.save()           
        return render(request, 'applogin/registrationsuccess.html', {'form': form})

class RequestpwdFormView(View):
    form_class = RequestpwdForm
    template_name = 'applogin/requestpwd_form.html'

    # displays a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

class RegistrationSuccessView(View):
    model = School
    template_name = 'applogin/registrationsuccess.html'   
    def get(self, request):
        return render(request, 'applogin/registrationsuccess.html', {'school': 'dummy@gmail.com'})