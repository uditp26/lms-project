from django.shortcuts import render, reverse, redirect
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.http import Http404
import os

# from django.contrib.auth.models import User
from applogin.models import User

from adminhome.models import Teacher, School, Student
from teacherhome.models import Attendance, Assignment
from time import gmtime, strftime
import datetime
import mimetypes

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

decorators = [cache_control(no_cache=True, must_revalidate=True, no_store=True), login_required(login_url='http:/127.0.0.1:8000/applogin/')]

# def download_file(request):
#     # fill these variables with real values

#     path = 'media/' + instance.school.school_code
#     path += '/Assignment/' + str(instance.class_number)+'/' + str(instance.subject)+'/'
#     fl_path = path
#     filename = str(assignment.subject) + str(assignment.assign_no) + '.pdf'

#     fl = open(fl_path, 'r’)
#     mime_type, _ = mimetypes.guess_type(fl_path)
#     response = HttpResponse(fl, content_type=mime_type)
#     response['Content-Disposition'] = "attachment; filename=%s" % filename
#         return response

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

@method_decorator(decorators, name='dispatch')
class AssignmentView(View):
    template_name = 'studenthome/all_assignment.html'

    def get(self, request):
        current_user = request.user
        student = Student.objects.get(user = current_user) 
        current_date = datetime.date.today()
        assign = Assignment.objects.filter(school = student.school, class_number = student.study, due_date__lte  = current_date).order_by('-due_date')
        bundle=dict()
        for i in assign:
            bundle[i.due_date] = i.subject
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

        return render(request, self.template_name, {'current_assign': current_assign})

@method_decorator(decorators, name='dispatch')      
class LogoutView(View):
    template_name = 'applogin/login.html'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('applogin:login'))



def index(request):
    text = request.GET.get("name")
    return text