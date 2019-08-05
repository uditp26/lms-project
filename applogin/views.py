from django.views import View
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RequestpwdForm, ResetpwdForm
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from .models import School
from applogin import otpgenerator

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
                    return redirect('adminhome:homepage')

        return render(request, self.template_name, {'form': form})

class SchoolView(CreateView):
	model  = School
	fields = [ "name", "email", "school_name", "school_address_line_1", "line_2", "city", "district", "state", "principal_name", "principal_email"]

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

        if form.is_valid():
            email = form.cleaned_data['email']

            # otp = getOTP(timestamp)
            otp = "1234"
            

            # python -m smtpd -n -c DebuggingServer localhost:1025

            send_mail(
                'App - Request for password change',
                'Here\'s your requested OTP for password change: ' + otp + '. \n This OTP will remain valid for 30 mins.',
                'admin-mail@app.com',
                [email],
                fail_silently=False,
            )

            return HttpResponseRedirect(reverse('applogin:resetpwd'))

        return render(request, self.template_name, {'form': form})

class ResetpwdFormView(View):
    form_class = ResetpwdForm
    template_name = 'applogin/resetpwd_form.html'

    # displays a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # logic for storing the new password
            pass

        return render(request, self.template_name, {'form': form})
        