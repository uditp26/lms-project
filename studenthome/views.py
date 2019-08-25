from django.shortcuts import render, reverse, redirect
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.http import Http404
import os
from django.contrib.auth.models import User
from adminhome.models import Teacher, School, Student
from teacherhome.models import ClassAttendance, Assignment, Student
from time import gmtime, strftime

class HomepageView(View):
    showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
    # print(showtime.split(' ')[0])
    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            student = 
            if student1.school.is_registered is True:
                bundle = {'Student':student1}
                return render(request, self.template_name, {'bundle': bundle})
            else:
                return redirect('studenthome:studenthome')

class AttendanceView(View):
    template_name = 'studenthome/attendance.html'

    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            student = Attendance.objects.get(school_admin=current_user)
            if student.school.is_registered is True:
                bundle = {'Student':student}
                return render(request, self.template_name, {'bundle': bundle})
            else:
                return redirect('adminhome:registerSchool')

class AssignmentView(View):
    template_name = 'studenthome/current_assignment.html'

    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            assign = Assignment.objects.get(school_admin=current_user)
            if assign.school.is_registered is True:
                bundle = {'Student':assign}
                return render(request, self.template_name, {'bundle': bundle})
            else:
                return redirect('adminhome:assignment')

class CurrentassignmentView(View):
    template_name = 'studenthome/current_assignment.html'

    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            assign = Assignment.objects.get(school_admin=current_user)
            if assign.school.is_registered is True:
                bundle = {'Student':assign}
                return render(request, self.template_name, {'bundle': bundle})
            else:
                return redirect('adminhome:assignment')