from django.shortcuts import render, reverse, redirect
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.http import Http404
import os

# from django.contrib.auth.models import User
from applogin.models import User

from adminhome.models import Teacher, School, Student, Principal
from teacherhome.models import Attendance, Assignment, Marksdetails
from principalhome.models import Announcement

from time import gmtime, strftime
import datetime
import mimetypes

#show pdf
from django.contrib import messages
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

decorators = [cache_control(no_cache=True, must_revalidate=True, no_store=True), login_required(login_url='http://127.0.0.1:8000/applogin/')]

@method_decorator(decorators, name='dispatch') #if you go back after login it will give error
class TeacherhomepageView(View):
    template_name = 'studenthome/homepage.html'
    
    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            student = Student.objects.get(user = current_user) 

            name = str(student.first_name)+' '+str(student.last_name)
            enrolment_no = student.enrolment_no
            roll_no = student.roll_no
            date_of_birth = student.date_of_birth
            email = student.email
            address = student.address
            study = student.study

            bundle = {'Name':name, 'Enrolment no.': enrolment_no, 'Roll no.':roll_no, 'class': study,  'Date of Birth':date_of_birth, 'Email': email, 'Address': address}
            return render(request, self.template_name, {'student':bundle}) 
            
@method_decorator(decorators, name='dispatch')
class AttendanceView(View):
    template_name = 'studenthome/attendance.html'

    def get(self, request):
        current_user = request.user
        student = Student.objects.get(user = current_user) 
        attendance = Attendance.objects.filter(school = student.school, roll_no = student.roll_no, study = student.study)
        return render(request, self.template_name, {'attendance': attendance})

class MarksView(View):
    template_name = 'studenthome/marks_view.html'

    def get(self, request):
        current_user = request.user
        student = Student.objects.get(user = current_user) 

        teacher = Teacher.objects.get(class_teacher_of = student.study, school = student.school)  
        marksheets = Marksdetails.objects.filter(roll_no = student.roll_no, teacher = teacher)

        bundle = dict()
        key = 1
        for a in marksheets:
            bundle[key] = a
            key += 1 
        return render(request, self.template_name, {'marksheets': bundle})

@method_decorator(decorators, name='dispatch')
class AssignmentView(View):
    template_name = 'studenthome/all_assignment.html'

    def get(self, request):
        current_user = request.user
        student = Student.objects.get(user = current_user) 
        current_date = datetime.date.today()
        assign = Assignment.objects.filter(school = student.school, class_number = student.study, due_date__lte  = current_date).order_by('-due_date')
        bundle=dict()
        key = 1
        for a in assign:
            bundle[key] = a
            key += 1 
        return render(request, self.template_name, {'bundle': bundle})

# For current pending assignments
@method_decorator(decorators, name='dispatch')
class CurrentassignmentView(View):
    template_name = 'studenthome/current_assignment.html'

    def get(self, request):
        current_user = request.user
        student = Student.objects.get(user = current_user)
        current_date = datetime.date.today()
        
        current_assign = Assignment.objects.filter(school = student.school, class_number = student.study, due_date__gte  = current_date).order_by('due_date')

        bundle=dict()
        key = 1
        for a in current_assign:
            bundle[key] = a
            key += 1 
        return render(request, self.template_name, {'bundle': bundle})

@method_decorator(decorators, name='dispatch')      
class LogoutView(View):
    template_name = 'applogin/login.html'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('applogin:login'))

@method_decorator(decorators, name='dispatch')
class AnnouncementView(View):
    template_name = 'studenthome/announcements.html'

    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            # student = Student.objects.get(user = current_user)
            current_date = datetime.date.today()
            announcement_type1 = Announcement.objects.filter(audience="Students", expiry_date__gte = current_date)
            announcement_type2 = Announcement.objects.filter(audience="All", expiry_date__gte = current_date)
            
            announcements = announcement_type1 | announcement_type2

            return render(request, self.template_name, {'announcements': announcements})

@method_decorator(decorators, name='dispatch')
class AnnouncementDetailView(View):
    template_name = 'studenthome/announcement_detail.html'

    def get(self, request, announcement):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            school = request.user.school
            principal = Principal.objects.get(school = school)
           
            announcement1 = Announcement.objects.get(announcer = principal, audience="Students")
            announcement2 = Announcement.objects.get(announcer = principal, audience="All")
            announcement = announcement1 | announcement2

            return render(request, self.template_name, {'announcement': announcement})

def index(request):
    text = request.GET.get("name")
    return text
