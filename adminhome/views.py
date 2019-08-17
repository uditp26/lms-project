from django.shortcuts import render, reverse, redirect
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from .models import LocalAdmin, Student, Teacher, Principal, Parent, School
from .forms import AddstudentForm, AddteacherForm, RegisterschoolForm, AddprincipalForm
from django.http import Http404
import os
# from django.contrib import messages

class HomepageView(View):
    template_name = 'adminhome/homepage.html'

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
            clss = 'Class ' + str(c)
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
            school = School.objects.get(school_admin=current_user)
            prefix = str(form.cleaned_data['admission_date'])[:4]

            all_students = len(Student.objects.all())
            enrolment_no = prefix + '' + str(all_students + 1)

            student.enrolment_no = enrolment_no

            student.school = school
            
            student.save()
            
            # Display a message for successful registration 

            # messages.add_message(request, messages.INFO, 'Student registered.')
            # return render(request, self.template_name, {'student_flag': True})

            return redirect('adminhome:addstudent')

        return render(request, self.template_name, {'form': form})

class StudentIndexView(generic.ListView):
    template_name = 'adminhome/students_index.html'

    def get_queryset(self):
        return Student.objects.all()

class TeacherView(View):
    template_name = 'adminhome/teachers.html'

    def get(self, request):
        current_user = request.user
        school = School.objects.get(school_admin=current_user)

        teachers = Teacher.objects.filter(school=school)
        bundle = dict()

        for t in teachers:
            t_name = t.first_name + ' ' + t.last_name
            # Issue : Two teachers with the same name
            bundle[t_name] = t.subject

        return render(request, self.template_name, {'teachers': bundle})

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
            teacher = form.save(commit=False)
            school = School.objects.get(school_admin=current_user)

            teacher.school = school
            
            teacher.save()

            # Display a message for successful registration 
            
            return redirect('adminhome:addteacher')

        return render(request, self.template_name, {'form': form})

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

                principal.school = school
                principal.save()

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
