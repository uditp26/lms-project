from django.shortcuts import render, reverse, redirect
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from .models import LocalAdmin, Student, Teacher, Principal, Parent, School
from .forms import AddstudentForm, AddteacherForm, RegisterschoolForm, AddprincipalForm
from django.contrib.auth.models import User
from django.http import Http404
from django.core.mail import send_mail
import os
# from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

from django.template import loader

import string
from random import *
min_char = 8
max_char = 12

def createNewUser(email, first_name, last_name):
    username = email.split('@')[0]
    # check for unique username
    similar_users = len(User.objects.filter(username=username))
    if similar_users != 0:
        new_username = username + '_' + str(similar_users)
        i = 0
        while len(User.objects.filter(username=new_username)) != 0:
            i += 1
            new_username = username + '_' + str(similar_users  + i)
        username = new_username

    # generate a random string
    allchar = string.ascii_letters + string.punctuation + string.digits
    password = "".join(choice(allchar) for x in range(randint(min_char, max_char)))

    new_user = User(username=username, email=email, first_name=first_name, last_name=last_name)
    new_user.set_password(password)
    new_user.save()

    return new_user, username

def sendSetPasswordMail(request, new_user, first_name, username, current_user, email):

    current_site = get_current_site(request)
    domain = current_site.domain
    uid = urlsafe_base64_encode(force_bytes(new_user.pk))
    token = default_token_generator.make_token(new_user)
    protocol = 'http'

    if type(token) != str:
        token = token[0]

    html_message = loader.render_to_string(
    'adminhome/user_registration_email.html',
    {
        'name': first_name,
        'username': username,
        'protocol': protocol,
        'domain':  domain,
        'uid': uid,
        'token': token
    })

    # print(html_message)

    # re-configure connection/email backend dynamically!

    send_mail(
        'Account Registration',
        '',
        str(current_user),
        [email],
        fail_silently=False,
        html_message=html_message
    )

class HomepageView(View):
    template_name = 'adminhome/homepage.html'

    # def get(self, request, username):
    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            school = School.objects.get(school_admin=current_user)

            if school.is_registered is True:
                students = len(Student.objects.filter(school=school))
                teachers = len(Teacher.objects.filter(school=school))
                bundle = {'user':current_user, 'school':str(school), 'students':students, 'teachers':teachers}
                return render(request, self.template_name, {'bundle': bundle})
            else:
                return redirect('adminhome:registerSchool')

class RegisterschoolFormView(View):
    form_class = RegisterschoolForm
    template_name = 'adminhome/registerschool_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        current_user = request.user
        form = self.form_class(request.POST)

        if form.is_valid():
            school_name = form.cleaned_data['school_name']
            class_upto = form.cleaned_data['class_upto']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            district = form.cleaned_data['district']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']

            school = School.objects.get(school_admin=current_user.pk)
            school.school_name = school_name
            school.class_upto = class_upto
            school.address= address
            school.city = city
            school.district = district
            school.state = state
            school.pincode = pincode
            school.is_registered = True
            school.has_principal = False

            school.save()

            dir_name = school.school_code + '/'
            os.mkdir(os.path.join('media/', dir_name))
            os.mkdir(os.path.join('media/' + dir_name, 'Teachers/'))
            os.mkdir(os.path.join('media/' + dir_name, 'Students/'))
            os.mkdir(os.path.join('media/' + dir_name, 'Principal/'))

            return redirect('adminhome:homepage')

        return render(request, self.template_name, {'form': form})

class StudentView(View):
    template_name = 'adminhome/students.html'

    def get(self, request):
        current_user = request.user
        school = School.objects.get(school_admin=current_user)

        NC = school.class_upto
        bundle = dict()

        for c in range(1, NC+1):
            clss = 'Class_' + str(c)
            school_students = Student.objects.filter(school=school)
            class_count = len(school_students.filter(study=c))
            bundle[clss] = class_count

        return render(request, self.template_name, {'class_dict': bundle})

class AddstudentFormView(View):
    form_class = AddstudentForm
    template_name = 'adminhome/addstudent_form.html'

    # displays a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        current_user = request.user

        if form.is_valid():
            student = form.save(commit=False)

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            # username = email.split('@')[0]
            # # check for unique username
            # similar_users = len(User.objects.filter(username=username))
            # if similar_users != 0:
            #     new_username = username + '_' + str(similar_users)
            #     i = 0
            #     while len(User.objects.filter(username=new_username)) != 0:
            #         i += 1
            #         new_username = username + '_' + str(similar_users  + i)
            #     username = new_username

            # # generate a random string
            # allchar = string.ascii_letters + string.punctuation + string.digits
            # password = "".join(choice(allchar) for x in range(randint(min_char, max_char)))

            # new_user = User(username=username, email=email, first_name=first_name, last_name=last_name)
            # new_user.set_password(password)
            # new_user.save()

            new_user, username = createNewUser(email, first_name, last_name)

            school = School.objects.get(school_admin=current_user)
            prefix = str(form.cleaned_data['admission_date'])[:4]

            all_students = len(Student.objects.filter(school=school).filter(enrolment_no__startswith=prefix))
            enrolment_no = prefix + '' + str(all_students + 1)

            student.enrolment_no = enrolment_no

            student.school = school
            student.user = new_user
            
            student.save()

            sendSetPasswordMail(request, new_user, first_name, username, current_user, email)
            
            # Display a message for successful registration 

            # messages.add_message(request, messages.INFO, 'Student registered.')
            # return render(request, self.template_name, {'student_flag': True})

            return redirect('adminhome:addstudent')

        return render(request, self.template_name, {'form': form})

class StudentIndexView(View):
    template_name = 'adminhome/students_index.html'

    def get(self, request, clss):
        current_user = request.user
        school = School.objects.get(school_admin=current_user)

        students = Student.objects.filter(school=school)
        cls_no = int(clss[6:])

        class_students = students.filter(study=cls_no)

        return render(request, self.template_name, {'class_students': class_students, 'clss':clss})

class StudentDetailView(View):
    template_name = 'adminhome/students_detail.html'

    def get(self, request, clss, student):
        school = request.user.school
        study = int(clss[6:])
        stud_arr = student.split('-')
        fname = stud_arr[0]
        lname = stud_arr[1]
        student = Student.objects.get(school=school, study=study, first_name=fname, last_name=lname)
        return render(request, self.template_name, {'student':student})    

class TeacherView(View):
    template_name = 'adminhome/teachers.html'

    def get(self, request):
        current_user = request.user
        school = School.objects.get(school_admin=current_user)

        teachers = Teacher.objects.filter(school=school)

        if len(teachers) > 0:
            return render(request, self.template_name, {'teachers': teachers})

        return render(request, self.template_name)

class AddteacherFormView(View):
    form_class = AddteacherForm
    template_name = 'adminhome/addteacher_form.html'

    # displays a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        current_user = request.user

        if form.is_valid():
            # class_taecher_of field should be enforced only when is_class_teacher is selected!
            teacher = form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            # username = email.split('@')[0]
            # # check for unique username
            # similar_users = len(User.objects.filter(username=username))
            # if similar_users != 0:
            #     new_username = username + '_' + str(similar_users)
            #     i = 0
            #     while len(User.objects.filter(username=new_username)) != 0:
            #         i += 1
            #         new_username = username + '_' + str(similar_users  + i)
            #     username = new_username

            # # generate a random string
            # allchar = string.ascii_letters + string.punctuation + string.digits
            # password = "".join(choice(allchar) for x in range(randint(min_char, max_char)))

            # new_user = User(username=username, email=email, first_name=first_name, last_name=last_name)
            # new_user.set_password(password)
            # new_user.save()

            new_user, username = createNewUser(email, first_name, last_name)

            school = School.objects.get(school_admin=current_user)

            teacher.school = school
            teacher.user = new_user

            teacher.save()

            sendSetPasswordMail(request, new_user, first_name, username, current_user, email)

            # create one-time link: protocol://domain/url/uidb64=uid/token=token/

            # current_site = get_current_site(request)
            # domain = current_site.domain
            # uid = urlsafe_base64_encode(force_bytes(new_user.pk))
            # token = default_token_generator.make_token(new_user),
            # protocol = 'http'

            # # send mail to teacher

            # # print(token)

            # html_message = loader.render_to_string(
            # 'adminhome/user_registration_email.html',
            # {
            #     'name': first_name,
            #     'username': username,
            #     'protocol': protocol,
            #     'domain':  domain,
            #     'uid': uid,
            #     'token': token[0]
            # })

            # # print(html_message)

            # # re-configure connection/email backend dynamically!

            # send_mail(
            #     'Account Registration',
            #     '',
            #     str(current_user),
            #     [email],
            #     fail_silently=False,
            #     html_message=html_message
            # )
            
            # Display a message for successful registration

            return redirect('adminhome:addteacher')

        return render(request, self.template_name, {'form': form})

class TeacherDetailView(View):
    template_name = 'adminhome/teachers_detail.html'

    def get(self, request, teacher):
        school = request.user.school
        name_arr = teacher.split('-')
        fname = name_arr[0]
        lname = name_arr[1]
        teacher = Teacher.objects.get(school=school, first_name=fname, last_name=lname)
        return render(request, self.template_name, {'teacher': teacher})

class PrincipalView(View):
    template_name = 'adminhome/principal.html'

    def get(self, request):
        current_user = request.user
        school = School.objects.get(school_admin=current_user)

        if school.has_principal is True:
            principal = Principal.objects.get(school=school)
            principal_name = principal.first_name + ' ' + principal.last_name
            joining_date = principal.joining_date
            email = principal.email
            phone = principal.phone
            bundle = {'Name':principal_name, 'Email':email, 'Phone':phone}
            return render(request, self.template_name, {'principal':bundle})
        else:
            return redirect('adminhome:addPrincipal')

class AddprincipalFormView(View):
    form_class = AddprincipalForm
    template_name = 'adminhome/addprincipal_form.html'

    # displays a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        current_user = request.user

        if form.is_valid():
            principal = form.save(commit=False)

            is_teacher = form.cleaned_data['is_teacher']
            subject = form.cleaned_data['subject']

            if is_teacher is False or is_teacher is True and subject != "":
                school = School.objects.get(school_admin=current_user)

                school.has_principal = True
                school.save()

                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']

                # username = email.split('@')[0]
                # # check for unique username
                # similar_users = len(User.objects.filter(username=username))
                # if similar_users != 0:
                #     new_username = username + '_' + str(similar_users)
                #     i = 0
                #     while len(User.objects.filter(username=new_username)) != 0:
                #         i += 1
                #         new_username = username + '_' + str(similar_users  + i)
                #     username = new_username

                # # generate a random string
                # allchar = string.ascii_letters + string.punctuation + string.digits
                # password = "".join(choice(allchar) for x in range(randint(min_char, max_char)))

                # new_user = User(username=username, email=email, first_name=first_name, last_name=last_name)
                # new_user.set_password(password)
                # new_user.save()

                new_user, username = createNewUser(email, first_name, last_name)

                principal.school = school
                principal.user = new_user
                principal.save()

                sendSetPasswordMail(request, new_user, first_name, username, current_user, email)

                # Display a message for successful registration
                
                return redirect('adminhome:principal')
            else:
                form.add_error('subject', "Subject field can't be empty.")

        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    template_name = 'applogin/login.html'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('applogin:login'))
