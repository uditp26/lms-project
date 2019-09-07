from django.shortcuts import render, reverse, redirect
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.http import Http404
import os
from django.contrib.auth.models import User
from adminhome.models import Teacher, School, Student
from teacherhome.models import Attendance, Assignment
from time import gmtime, strftime

class TeacherhomepageView(View):
    template_name = 'studenthome/homepage.html'
    
    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            student = Student.objects.get(user = current_user) 

            name = str(student.first_name)+' '+str(student.last_name)
            enrollment_no = student.enrollment_no
            roll_no = student.roll_no
            date_of_birth = student.date_of_birth
            email = student.email
            address = student.address
            study = student.study

            bundle = {'name':name, 'enrollment_no': enrollment_no, 'roll_no':roll_no, 'study': study,  'date_of_birth':date_of_birth, 'email': email, 'address': address}
            return render(request, self.template_name, {'student':bundle}) 
            
        

# class AttendanceView(View):
#     template_name = 'studenthome/attendance.html'

#     def get(self, request):
#         current_user = request.user
#         if str(current_user) is 'AnonymousUser':
#             raise Http404
#         else:
#             student = Attendance.objects.get(school_admin=current_user)
#             if student.school.is_registered is True:
#                 bundle = {'Student':student}
#                 return render(request, self.template_name, {'bundle': bundle})
#             else:
#                 return redirect('adminhome:registerSchool')

# class AssignmentView(View):
#     template_name = 'studenthome/current_assignment.html'

#     def get(self, request):
#         current_user = request.user
#         if str(current_user) is 'AnonymousUser':
#             raise Http404
#         else:
#             assign = Assignment.objects.get(school_admin=current_user)
#             if assign.school.is_registered is True:
#                 bundle = {'Student':assign}
#                 return render(request, self.template_name, {'bundle': bundle})
#             else:
#                 return redirect('adminhome:assignment')

# class CurrentassignmentView(View):
#     template_name = 'studenthome/current_assignment.html'

#     def get(self, request):
#         current_user = request.user
#         if str(current_user) is 'AnonymousUser':
#             raise Http404
#         else:
#             assign = Assignment.objects.get(school_admin=current_user)
#             if assign.school.is_registered is True:
#                 bundle = {'Student':assign}
#                 return render(request, self.template_name, {'bundle': bundle})
#             else:
#                 return redirect('adminhome:assignment')