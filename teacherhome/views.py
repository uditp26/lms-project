from django.shortcuts import render, reverse, redirect
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from .models import Assignment, Attendance
from .forms import AddassignForm, AttendanceForm
from adminhome.models import School, Student, Teacher
from collections import defaultdict
from django.urls import reverse_lazy
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import datetime

class TeacherhomepageView(View):
    template_name = 'teacherhome/teacherhomepage.html'
    
    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            teacher = Teacher.objects.get(user = current_user) 
            name = str(teacher.first_name)+' '+str(teacher.last_name)
            subject = teacher.subject
            if teacher.is_class_teacher == True:
                class_number = teacher.class_teacher_of
                no_of_students = len(Student.objects.filter(school = teacher.school, study = class_number)) 
                bundle = {'name':name, 'subject': subject, 'class_number':class_number, 'no_of_students':no_of_students}
                return render(request, self.template_name, {'teacher':bundle}) 
            else:
                bundle = {'name':name, 'subject': subject}
                return render(request, self.template_name, {'teacher':bundle})

class AddassignFormView(View):
    form_class = AddassignForm
    template_name = 'teacherhome/addassign_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        current_user = request.user
        teacher = Teacher.objects.get(user = current_user)  
        if form.is_valid():
            addassign = form.save(commit = False)
            subject = teacher.subject
            assignment_no = len(Assignment.objects.filter(assigned_by=teacher, subject=subject)) + 1
            addassign.assign_number = assignment_no
            addassign.assigned_by = teacher
            addassign.save() 
            return redirect('teacherhome:view_assign')
        return render(request, self.template_name, {'form': form})  

class AssignmentView(View):
    template_name = 'teacherhome/assignment_view.html'

    def get(self, request):
        current_user = request.user
        teacher = Teacher.objects.get(user = current_user)  
        assignment = Assignment.objects.filter(assigned_by=teacher)

        bundle = dict()
        for a in assignment:
            a_class = a.class_number
            bundle[a_class] = a 

        return render(request, self.template_name, {'assignment': bundle})

class AttendanceFormView(View):
    form_class = AttendanceForm
    template_name = 'teacherhome/attendance_form.html'
    
    def get(self, request):
        #Enable attendance link only for class teacher
        
        roll_no_list = []
        current_user = request.user
        teacher = Teacher.objects.get(user = current_user)
        students = Student.objects.filter(school = teacher.school,  study = teacher.class_teacher_of)
        school = Teacher.objects.get(school = teacher.school)
        
        for s in students:
            roll_no_list.append(s.roll_no)
        
        form = self.form_class(request.GET, extra = roll_no_list) 
        
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        roll_no_list = []
        current_user = request.user
        teacher = Teacher.objects.get(user = current_user)
        students = Student.objects.filter(school = teacher.school,  study = teacher.class_teacher_of)
        
        for s in students:
            roll_no_list.append(s.roll_no)
        
        form = self.form_class(request.POST, extra = roll_no_list)

        if form.is_valid():
            
            for (label, response) in form.extra_responses(): 
                if response == "2":
                    student = Student.objects.get(school = teacher.school, roll_no = label)
                    date = datetime.date.today()
                    att = Attendance(school = teacher.school, enrolment_no = student.enrolment_no, absent_on = date)
                    att.save()

            return redirect('teacherhome:attendance')

        return render(request, self.template_name, {'form': form})

class SendAttendanceView(View):
    template_name = 'teacherhome/sendattendance.html'
    def post(self, request):
        return render(request, self.template_name)

# class SendMessageView(View):
#     form_class = SendMessageForm
#     template_name = 'teacherhome/sendmessage_form.html'

#     # display blank form
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})

    # process form data
    # def post(self, request):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         sendmessage = form.save(commit = False)
    #         sendmessage.save() # save to the database
        
    # return render(request, self.template_name, {'form': form})

class SendResultView(View):
    template_name = 'teacherhome/sendresult_form.html'
    def get(self, request):
        return render(request, self.template_name)

class NotificationView(View):
    template_name = 'teacherhome/notification.html'
    # context = {'admin': LocalAdmin.objects.get(pk=1)} # use filter()
    def get(self, request):
        current_user = request.user
        return render(request, self.template_name, {'current_user': current_user})
class ScheduleView(View):
    template_name = 'teacherhome/schedule.html'
    # context = {'admin': LocalAdmin.objects.get(pk=1)} # use filter()
    def get(self, request):
        current_user = request.user
        return render(request, self.template_name, {'current_user': current_user})

class LogoutView(View):
    template_name = 'applogin/login.html'
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('applogin:login'))

class TeacherUpdateView(UpdateView):
    model = Teacher
    fields = ['first_name', 'last_name', 'date_of_birth', 'joining_date', 'email', 'phone', 'is_class_teacher', 'subject', 'resume']










