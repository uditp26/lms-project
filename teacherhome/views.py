from django.shortcuts import render, reverse, render
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from .models import Assignment, ClassAttendance, SendAttendance
from .forms import AddassignForm, ClassAttendanceForm, SendMessageForm

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
        form = self.form_class(request.POST)

        if form.is_valid():

            addassign = form.save(commit = False)
            addassign.save() # save to the database
        
        return render(request, self.template_name, {'form': form})  

class ClassAttendanceView(View):
    form_class = ClassAttendanceForm
    template_name = 'teacherhome/classattendance_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            classattendence = form.save(commit = False)
            classattendence.save() # save to the database
        
        return render(request, self.template_name, {'form': form})

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