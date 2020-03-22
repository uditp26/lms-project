from django.shortcuts import render, reverse, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from adminhome.models import Student, Teacher, Principal, School
from django.http import Http404
from .forms import AnnouncementForm
from .models import Announcement
import datetime

# from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

decorators = [cache_control(no_cache=True, must_revalidate=True, no_store=True), login_required(login_url='http://185.201.9.188:80/lms/applogin/')]

@method_decorator(decorators, name='dispatch')
class HomepageView(View):
    template_name = 'principalhome/homepage.html'

    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            principal = Principal.objects.get(user = current_user)
            school = principal.school
            students = len(Student.objects.filter(school=school))
            teachers = len(Teacher.objects.filter(school=school))
            bundle = {'user':current_user, 'school':str(school), 'students':students, 'teachers':teachers}
            return render(request, self.template_name, {'bundle': bundle})

@method_decorator(decorators, name='dispatch')
class StudentView(View):
    template_name = 'principalhome/students.html'

    def get(self, request):
        current_user = request.user
        principal = Principal.objects.get(user = current_user)
        school = principal.school

        NC = school.class_upto
        bundle = dict()

        for c in range(1, NC+1):
            clss = 'Class_' + str(c)
            school_students = Student.objects.filter(school=school)
            class_count = len(school_students.filter(study=c))
            bundle[clss] = class_count

        return render(request, self.template_name, {'class_dict': bundle})

@method_decorator(decorators, name='dispatch')
class StudentIndexView(View):
    template_name = 'principalhome/students_index.html'

    def get(self, request, clss):
        current_user = request.user
        principal = Principal.objects.get(user = current_user)
        school = principal.school

        students = Student.objects.filter(school=school)
        cls_no = int(clss[6:])

        class_students = students.filter(study=cls_no)

        return render(request, self.template_name, {'class_students': class_students, 'clss':clss})

@method_decorator(decorators, name='dispatch')
class StudentDetailView(View):
    template_name = 'principalhome/students_detail.html'

    def get(self, request, clss, student):
        current_user = request.user
        principal = Principal.objects.get(user = current_user)
        school = principal.school
        study = int(clss[6:])
        stud_arr = student.split('-')
        fname = stud_arr[0]
        lname = stud_arr[1]
        student = Student.objects.get(school=school, study=study, first_name=fname, last_name=lname)
        return render(request, self.template_name, {'student':student})    

@method_decorator(decorators, name='dispatch')
class TeacherView(View):
    template_name = 'principalhome/teachers.html'

    def get(self, request):
        current_user = request.user
        principal = Principal.objects.get(user = current_user)
        school = principal.school

        teachers = Teacher.objects.filter(school=school)

        if len(teachers) > 0:
            return render(request, self.template_name, {'teachers': teachers})

        return render(request, self.template_name)

@method_decorator(decorators, name='dispatch')
class TeacherDetailView(View):
    template_name = 'principalhome/teachers_detail.html'

    def get(self, request, teacher):
        current_user = request.user
        principal = Principal.objects.get(user = current_user)
        school = principal.school
        name_arr = teacher.split('-')
        fname = name_arr[0]
        lname = name_arr[1]
        teacher = Teacher.objects.get(school=school, first_name=fname, last_name=lname)
        return render(request, self.template_name, {'teacher': teacher})

@method_decorator(decorators, name='dispatch')
class AnnouncementView(View):
    template_name = 'principalhome/announcements.html'

    def get(self, request):
        current_user = request.user
        principal = Principal.objects.get(user = current_user)
        current_date = datetime.date.today()
        announcements = Announcement.objects.filter(announcer=principal, expiry_date__gte = current_date).order_by('-expiry_date')
        return render(request, self.template_name, {'announcements': announcements})


@method_decorator(decorators, name='dispatch')
class AnnouncementFormView(View):
    form_class = AnnouncementForm
    template_name = 'principalhome/announcement_form.html'

    # displays a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        current_user = request.user
        principal = Principal.objects.get(user = current_user)
        current_date = datetime.date.today()

        if form.is_valid():
            subject = form.cleaned_data['subject']
            expiry_date = form.cleaned_data['expiry_date']
            audience = form.cleaned_data['audience']
            message = form.cleaned_data['message']

            if audience == "1":
                audience = "Teachers"
            elif audience == "2":
                audience = "Students"
            else:
                audience = "All"

            announcement = Announcement(announcer=principal, subject=subject, announcement_date=current_date, expiry_date=expiry_date, audience=audience, message=message)
            announcement.save()

            return redirect('principalhome:announcements')

        return render(request, self.template_name, {'form': form})
