from django.shortcuts import render, reverse, redirect
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from .models import LocalAdmin, Student, Teacher, Principal, Parent, School
from .forms import AddstudentForm, AddteacherForm, RegisterschoolForm
from django.http import Http404
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
                bundle = {'user':current_user, 'school':str(school)}
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
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            district = form.cleaned_data['district']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']

            school = School.objects.get(school_admin=current_user.pk)
            school.school_name = school_name
            school.address= address
            school.city = city
            school.district = district
            school.state = state
            school.pincode = pincode
            school.is_registered = True

            school.save()

            return redirect('adminhome:homepage')

        return render(request, self.template_name, {'form': form})

class StudentView(View):
    template_name = 'adminhome/students.html'

    def get(self, request):
        return render(request, self.template_name)

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
            
            print('Enrolment No:' + enrolment_no)

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
        return render(request, self.template_name) 

class LogoutView(View):
    template_name = 'applogin/login.html'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('applogin:login'))
