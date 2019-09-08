from django.views import View
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RequestpwdForm, ResetpwdForm, RegistrationForm, PasswordResetForm, SetPasswordForm
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse
from django import forms
from adminhome.models import School


from urllib.parse import urlparse, urlunparse
from django.conf import settings

from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

UserModel = get_user_model()

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
                    print(user)
                    print(radio_btn)
                    print(type(radio_btn))
                    login(request, user)
                    # redirect to respective page
                    if radio_btn == '1':
                        return redirect('studenthome:studenthome')
                    elif radio_btn == '2':
                        return redirect('teacherhome:teacher_homepage')
                    elif radio_btn == '3': 
                        return redirect('')
                    elif radio_btn == '4':
                        return redirect('')
                    elif radio_btn == '5':
                        return redirect('adminhome:homepage')
                    # Add else condition
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

# Class-based password reset views
# - PasswordResetView sends the mail
# - PasswordResetDoneView shows a success message for the above
# - PasswordResetConfirmView checks the link the user clicked and
#   prompts for a new password
# - PasswordResetCompleteView shows a success message for the above

class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class PasswordResetView(PasswordContextMixin, FormView):
    template_name = 'applogin/password_reset_form.html'
    email_template_name = 'applogin/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'applogin/password_reset_subject.txt'
    success_url = reverse_lazy('applogin:password_reset_done')
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = 'applogin/password_reset_done.html'
    title = _('Password reset sent')


class PasswordResetConfirmView(PasswordContextMixin, FormView):
    template_name = 'applogin/password_reset_confirm.html'
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    success_url = reverse_lazy('applogin:password_reset_complete')
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == INTERNAL_RESET_URL_TOKEN:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, INTERNAL_RESET_URL_TOKEN)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context


class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'applogin/password_reset_complete.html'
    title = _('Password reset complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context


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
