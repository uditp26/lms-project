from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import User

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

            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    # return

        return render(request, self.template_name, {'form': form})

class UserView(CreateView):
	model  = User
	fields = [ "name", "email", "school_name", "school_address_line_1", 
               "line_2", "city", "district", "state", 
               "principal_name", "principal_email"]
