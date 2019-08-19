from django.views import View
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RequestpwdForm, ResetpwdForm, RegistrationForm
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from applogin import otpgenerator
from django.contrib.auth.models import User
from django.http import HttpResponse
from django import forms
from adminhome.models import School

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

        # determine which radio button is selected
        radio_btn = request.POST.get('radio_btn')

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # returns user objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    # redirect to respective page
                    if radio_btn == 1:
                        return redirect('')
                    elif radio_btn == 2:
                        return redirect('')
                    elif radio_btn == 3:
                        return redirect('')
                    elif radio_btn == 4:
                        return redirect('')
                    else:
                        return redirect('adminhome:homepage')
                        # return HttpResponseRedirect(reverse('adminhome:homepage', args=(username,)))
                else:
                    form.add_error('username', "User does not exist.")
            else:
                form.add_error('username', "User credentials did not match existing records.")

        return render(request, self.template_name, {'form': form})

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
            form_obj = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            confpwd = form.cleaned_data['password2']

            if password == confpwd:
                form_obj.save()

                user = User.objects.get(username=username)
                # generate a unique school code as primary key
                all_schools = School.objects.all()
                school_code = 'SCH' + '' + str(len(all_schools) + 1)
                print(school_code)
                school = School(school_code=school_code, school_admin=user)
                
                school.save()
                
                return render(request, 'applogin/registrationsuccess.html', {'form': form})
            else:
                form.add_error('confirm_password', "Password fields do not match.")

        return render(request, 'applogin/registration_form.html', {'form': form})

class RegistrationSuccessView(View):
    template_name = 'applogin/registrationsuccess.html'

    def get(self, request):
        return render(request, self.template_name)

# class RequestpwdFormView(View):
#     form_class = RequestpwdForm
#     template_name = 'applogin/requestpwd_form.html'

#     # displays a blank form
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})

#     # process form data
#     def post(self, request):
#         form = self.form_class(request.POST)

#         if form.is_valid():
#             email = form.cleaned_data['email']

#             # otp = getOTP(timestamp)
#             otp = "1234"
            

#             # python -m smtpd -n -c DebuggingServer localhost:1025

#             send_mail(
#                 'App - Request for password change',
#                 'Here\'s your requested OTP for password change: ' + otp + '. \n This OTP will remain valid for 30 mins.',
#                 'admin-mail@app.com',
#                 [email],
#                 fail_silently=False,
#             )

#             return redirect('applogin:requestpwdcnf')

#         return render(request, self.template_name, {'form': form})

# class RequestpwdcnfView(View):
#     template_name = 'applogin/requestpwdcnf.html'

#     def get(self, request):
#         return render(request, self.template_name)

# class ResetpwdFormView(View):
#     form_class = ResetpwdForm
#     template_name = 'applogin/resetpwd_form.html'

#     # displays a blank form
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})

#     # process form data
#     def post(self, request):
#         form = self.form_class(request.POST)

#         if form.is_valid():
#             # logic for storing the new password
#             # enforce strong passwrod constraints!
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             confpwd = form.cleaned_data['password_confirmation']

#             if password == confpwd:
#                 user = User.objects.get(username=username)
#                 if user is not None:
#                     user.set_password(password)
#                     user.save()
#                     return render(request, 'applogin/pwdchangesuccess.html', {'form': form})
#                 else:
#                     form.add_error('username', "User credentials did not match existing records.")
#             else:
#                 form.add_error('password_confirmation', "Password fields do not match.")

#         return render(request, self.template_name, {'form': form})

# class PwdChangeSuccessView(View):
#     template_name = 'applogin/pwdchangesuccess.html'

#     def get(self, request):
#         return render(request, self.template_name)
