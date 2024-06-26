from django.shortcuts import render, reverse, redirect
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from .models import LocalAdmin, Student, Teacher, Principal, Parent, School, Feecircular
from .forms import AddstudentForm, AddteacherForm, RegisterschoolForm, AddprincipalForm

# from django.contrib.auth.models import User
from applogin.models import User

from django.http import Http404
from django.core.mail import send_mail, EmailMessage
# from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from easy_pdf.rendering import render_to_pdf
from django.core.files.base import ContentFile
import datetime

# from django.contrib.auth.mixins import LoginRequiredMixin

from django.template import loader

import string
from random import *
min_char = 8
max_char = 12

decorators = [cache_control(no_cache=True, must_revalidate=True, no_store=True), login_required(login_url='http://127.0.0.1:8000/applogin/')]

def createNewUser(email, first_name, last_name, u_type):
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
    new_user.user_type = u_type
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

def sendFeeReminderMail(current_user, fee_obj, fileData):

    sch_obj = current_user.school
    students = Student.objects.filter(school=sch_obj)

    mailing_list = []
    for s in students:
        mailing_list.append(s.email)

    draft_email = EmailMessage(
        'Reminder for Fee Payment',
        'Please find attached the fee circular for this academic year. For fee payment and related queries, please visit the admin office. Please ignore if the fees has already been paid.',
        str(current_user),
        mailing_list,
    )

    draft_email.attach(fee_obj.file_name, fileData, 'application/pdf')
    draft_email.send()

@method_decorator(decorators, name='dispatch')
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

@method_decorator(decorators, name='dispatch')
class RegisterschoolFormView(View):
    form_class = RegisterschoolForm
    template_name = 'adminhome/registerschool_form.html'

    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
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

            try:
                old_school = School.objects.get(school_name=school_name, class_upto=class_upto, address=address, city=city, district=district, state=state, pincode=pincode)
                form.add_error('school_name', 'School already exists. Current Admin: ' + str(old_school.school_admin))
            except:
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

                return redirect('adminhome:homepage')

        return render(request, self.template_name, {'form': form})

@method_decorator(decorators, name='dispatch')
class StudentView(View):
    template_name = 'adminhome/students.html'

    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            school = School.objects.get(school_admin=current_user)

            NC = school.class_upto
            bundle = dict()

            for c in range(1, NC+1):
                clss = 'Class_' + str(c)
                school_students = Student.objects.filter(school=school)
                class_count = len(school_students.filter(study=c))
                bundle[clss] = class_count

            return render(request, self.template_name, {'class_dict': bundle})

@method_decorator(decorators, name='dispatch')
class AddstudentFormView(View):
    form_class = AddstudentForm
    template_name = 'adminhome/addstudent_form.html'

    # displays a blank form
    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
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
            study = form.cleaned_data['study']
            date_of_birth = form.cleaned_data['date_of_birth']
            admission_date = form.cleaned_data['admission_date']

            if admission_date <= date_of_birth:
                form.add_error('admission_date', 'Admission date can\'t be earlier than DOB.')
            else:
                new_user, username = createNewUser(email, first_name, last_name, 1)

                school = School.objects.get(school_admin=current_user)
                prefix = str(form.cleaned_data['admission_date'])[:4]

                all_students = len(Student.objects.filter(school=school).filter(enrolment_no__startswith=prefix))
                enrolment_no = prefix + '' + str(all_students + 1)
                student.enrolment_no = enrolment_no
                student.school = school
                student.user = new_user

                s_roll =  ""
                s_roll = s_roll + str(study)
                no_student = len(Student.objects.filter(school = school, study= study))  + 1
                student.roll_no = s_roll + str(no_student)

                student.save()
                sendSetPasswordMail(request, new_user, first_name, username, current_user, email)
            
                return redirect('adminhome:students')

        return render(request, self.template_name, {'form': form})

@method_decorator(decorators, name='dispatch')
class StudentIndexView(View):
    template_name = 'adminhome/students_index.html'

    def get(self, request, clss):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            school = School.objects.get(school_admin=current_user)

            students = Student.objects.filter(school=school)
            cls_no = int(clss[6:])

            class_students = students.filter(study=cls_no)

            return render(request, self.template_name, {'class_students': class_students, 'clss':clss})

@method_decorator(decorators, name='dispatch')
class StudentDetailView(View):
    template_name = 'adminhome/students_detail.html'

    def get(self, request, clss, enrolment_no):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            school = request.user.school
            study = int(clss[6:])
            # stud_arr = student.split('-')
            # fname = stud_arr[0]
            # lname = stud_arr[1]
            student = Student.objects.get(school=school, study=study, enrolment_no=enrolment_no)
            return render(request, self.template_name, {'student':student})    

@method_decorator(decorators, name='dispatch')
class TeacherView(View):
    template_name = 'adminhome/teachers.html'

    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            school = School.objects.get(school_admin=current_user)

            teachers = Teacher.objects.filter(school=school)

            if len(teachers) > 0:
                return render(request, self.template_name, {'teachers': teachers})

            return render(request, self.template_name)

@method_decorator(decorators, name='dispatch')
class AddteacherFormView(View):
    form_class = AddteacherForm
    template_name = 'adminhome/addteacher_form.html'

    # displays a blank form
    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        current_user = request.user

        if form.is_valid():
            
            is_class_teacher = form.cleaned_data['is_class_teacher']
            class_teacher_of = form.cleaned_data['class_teacher_of']
            date_of_birth = form.cleaned_data['date_of_birth']
            joining_date = form.cleaned_data['joining_date']

            if is_class_teacher is True and class_teacher_of is None:
                form.add_error('class_teacher_of', 'Please specify the class taught by the class teacher.')
            elif joining_date <= date_of_birth:
                form.add_error('joining_date', 'Joining date can\'t be earlier than DOB.')
            else:
                teacher = form.save(commit=False)
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']

                new_user, username = createNewUser(email, first_name, last_name, 2)

                school = School.objects.get(school_admin=current_user)
                # print("school_type : ", type(school))

                teacher.school = school
                teacher.user = new_user

                teacher.save()

                sendSetPasswordMail(request, new_user, first_name, username, current_user, email)
                
                # Display a message for successful registration

                return redirect('adminhome:teachers')

        return render(request, self.template_name, {'form': form})

@method_decorator(decorators, name='dispatch')
class TeacherDetailView(View):
    template_name = 'adminhome/teachers_detail.html'

    def get(self, request, username):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            school = request.user.school
            t_user = User.objects.get(username=username)
            teacher = Teacher.objects.get(user=t_user)
            return render(request, self.template_name, {'teacher': teacher})

@method_decorator(decorators, name='dispatch')
class PrincipalView(View):
    template_name = 'adminhome/principal.html'

    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
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

@method_decorator(decorators, name='dispatch')
class AddprincipalFormView(View):
    form_class = AddprincipalForm
    template_name = 'adminhome/addprincipal_form.html'

    # displays a blank form
    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
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
            date_of_birth = form.cleaned_data['date_of_birth']
            joining_date = form.cleaned_data['joining_date']

            if joining_date <= date_of_birth:
                form.add_error('joining_date', 'Joining date can\'t be earlier than DOB.')
            else: 
                if is_teacher is False or is_teacher is True and subject != "":
                    school = School.objects.get(school_admin=current_user)

                    school.has_principal = True
                    school.save()

                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    email = form.cleaned_data['email']

                    new_user, username = createNewUser(email, first_name, last_name, 3)

                    principal.school = school
                    principal.user = new_user
                    principal.save()

                    sendSetPasswordMail(request, new_user, first_name, username, current_user, email)

                    # Display a message for successful registration
                    
                    return redirect('adminhome:principal')
                else:
                    form.add_error('subject', "Subject field can't be empty.")

        return render(request, self.template_name, {'form': form})

@method_decorator(decorators, name='dispatch')
class FeeCircularsView(View):
    template_name = 'adminhome/feecirculars.html'

    def get(self, request):
        current_user = request.user
        fc_list = Feecircular.objects.filter(school_admin=current_user)
        return render(request, self.template_name, {'bundle': fc_list})

@method_decorator(decorators, name='dispatch')
class AddFeeCircularView(View):
    template_name = 'adminhome/addfeecircular_form.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        current_user = request.user
        tfee1 = request.POST.dict()['tfee1']
        tfee2 = request.POST.dict()['tfee2']
        tfee3 = request.POST.dict()['tfee3']
        dfee1 = request.POST.dict()['dfee1']
        dfee2 = request.POST.dict()['dfee2']
        dfee3 = request.POST.dict()['dfee3']
        ddate1 = request.POST.dict()['ddate1']
        ddate2 = request.POST.dict()['ddate2']
        ddate3 = request.POST.dict()['ddate3']
        notes = request.POST.dict()['notes']

        school = School.objects.get(school_admin=current_user)
        school_name = school.school_name

        ref_no = school.school_code + "/FCIR/#" + str(len(Feecircular.objects.all()) + 1) 
        date = datetime.date.today().strftime('%d-%m-%Y')
        bundle = {'school_name':school_name, 'ref_no':ref_no, 'date':date, 'tfee1':tfee1, 'tfee2':tfee2, 'tfee3':tfee3, 'dfee1':dfee1, 'dfee2':dfee2, 'dfee3':dfee3, 'ddate1':ddate1, 'ddate2':ddate2, 'ddate3':ddate3, 'notes':notes}

        fileData = render_to_pdf('adminhome/feecircular-template.html', {'bundle':bundle})

        file_data = ContentFile(fileData)
        file_name = "fcir_" + str(len(Feecircular.objects.all()) + 1) + "_" + str(date) + ".pdf"

        fee_obj = Feecircular(ref_no=ref_no, school_admin=current_user, date_of_issue=datetime.date.today().strftime('%Y-%m-%d'), file_name=file_name)
        fee_obj.save()
        fee_obj.pdf_ver.save(file_name, file_data)

        # Fee Reminder Mail
        sendFeeReminderMail(current_user, fee_obj, fileData)

        return HttpResponseRedirect(reverse('adminhome:feecirculars'))
