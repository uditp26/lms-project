from django.shortcuts import render, reverse, redirect
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from .models import Assignment, ClassAttendance, SendAttendance
from .forms import AddassignForm, ClassAttendanceForm, SendMessageForm
from adminhome.models import School, Student, Teacher
from collections import defaultdict
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class TeacherHomepageView(View):
    template_name = 'teacherhome/teacherHomepage.html'
    def get(self, request):
        current_user = request.user
        return render(request, self.template_name, {'admin': current_user})

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
        teacher = request.user

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
        teacher = request.user
        assignment = Assignment.objects.filter(assigned_by=teacher)
        # bundle = defaultdict(list)

        bundle = dict()
        for a in assignment:
            a_class = a.class_number
            bundle[a_class] = a 

        return render(request, self.template_name, {'assignment': bundle})
#____________________________________________Code will only work when teacher and student table are ready_____
class ClassAttendanceView(View):
    form_class = ClassAttendanceForm
    template_name = 'teacherhome/classattendance_form.html'
    
    def get(self, request):
        current_user = request.user
        students = Student.objects.get(school = current_user.school, study = current_user.study)

        bundle = dict()

        for s in students:
            s_name = s.first_name + ' ' + s.last_name
            # Issue : Two teachers with the same name
            bundle[s_name] = s.roll_number

        return render(request, self.template_name, {'student': bundle})

    # how to extract attendance 
    # def post(self, request):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         attendance = form.save(commit = False)
    #         attendance.save() # save to the database
        
    #     return render(request, self.template_name, {'form': form})
#______________________________________________________________________________________________________________

class SendAttendanceView(View):
    template_name = 'teacherhome/sendattendance.html'
    def post(self, request):
        return render(request, self.template_name)

class SendMessageView(View):
    form_class = SendMessageForm
    template_name = 'teacherhome/sendmessage_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            sendmessage = form.save(commit = False)
            sendmessage.save() # save to the database
        
        return render(request, self.template_name, {'form': form})

class SendResultView(View):
    template_name = 'teacherhome/sendresult_form.html'
    def get(self, request):
        return render(request, self.template_name)

class NotificationView(View):
    template_name = 'teacherhome/notification.html'
    # context = {'admin': LocalAdmin.objects.get(pk=1)} # use filter()
    def get(self, request):
        current_user = request.user
        return render(request, self.template_name, {'admin': current_user})
class ScheduleView(View):
    template_name = 'teacherhome/schedule.html'
    # context = {'admin': LocalAdmin.objects.get(pk=1)} # use filter()
    def get(self, request):
        current_user = request.user
        return render(request, self.template_name, {'admin': current_user})

class LogoutView(View):
    template_name = 'applogin/login.html'
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('applogin:login'))

class TeacherUpdateView(UpdateView):
    model = Teacher
    fields = ['first_name', 'last_name', 'date_of_birth', 'joining_date', 'email', 'phone', 'is_class_teacher', 'subject', 'resume']










