from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RequestpwdForm
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import School

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

        if form.is_valid():

            school = form.save(commit=False)

            # cleaned (normalized) data
            schoolname = form.cleaned_data['schoolname']
            password = form.cleaned_data['password']
            school.set_password(password)
            school.save()

            # returns School objects if credentials are correct
            school = authenticate(Schoolname=schoolname, password=password)

            if school is not None:

                if school.is_active:
                    login(request, school)
                    # return

        return render(request, self.template_name, {'form': form})

class SchoolView(CreateView):
	model  = School
	fields = [ "name", "email", "school_name", "school_address_line_1", 
               "line_2", "city", "district", "state", 
               "principal_name", "principal_email"]

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
