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

#show pdf
from django.contrib import messages
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings

#html to pdf 
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def sendSetPasswordMail(request, new_user, first_name, username, current_user, email):

    current_site = get_current_site(request)
    domain = current_site.domain
    uid = urlsafe_base64_encode(force_bytes(new_user.pk))
    token = default_token_generator.make_token(new_user)
    protocol = 'http'

    if type(token) != str:
        token = token[0]

    html_message = loader.render_to_string(
    'adminhome/user_registration_email.html',
    {
        'name': first_name,
        'username': username,
        'protocol': protocol,
        'domain':  domain,
        'uid': uid,
        'token': token
    })

    # print(html_message)

    # re-configure connection/email backend dynamically!

    send_mail(
        'Account Registration',
        '',
        str(current_user),
        [email],
        fail_silently=False,
        html_message=html_message
    )

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



class SeeAssignmentView(View):
    template_name = 'teacherhome/assignment_see.html'

    def get(self, request, path):
        print(path)
        filename =str(path).replace("_","/")
        rel_path = 'media/'+filename+".pdf"
        print(rel_path)
        return FileResponse(open(rel_path, 'rb'), content_type='application/pdf')
        # return render(request, self.template_name)

class AssignmentView(View):
    template_name = 'teacherhome/assignment_view.html'

    def get(self, request):
        current_user = request.user
        teacher = Teacher.objects.get(user = current_user)  
        assignment = Assignment.objects.filter(assigned_by = teacher)

        bundle = dict()
        key = 1
        for a in assignment:
            bundle[key] = a
            key += 1 

        return render(request, self.template_name, {'assignment': bundle})

class AttendanceFormView(View):
    form_class = AttendanceForm
    template_name = 'teacherhome/attendance_form.html'
    
    def get(self, request):
        #Enable attendance link only for class teacher
        
        roll_no_list = []
        current_user = request.user
        teacher = Teacher.objects.get(user = current_user)
        
        if teacher.is_class_teacher:
            students = Student.objects.filter(school = teacher.school,  study = teacher.class_teacher_of)
            school = Teacher.objects.get(school = teacher.school)
            
            for s in students:
                roll_no_list.append(s.roll_no)
            
            form = self.form_class(request.GET, extra = roll_no_list) 
            
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('teacherhome:notallowed')

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
                    student_name= student.first_name + ' ' +  student.last_name
                    att = Attendance(school = student.school, roll_no = student.roll_no, absent_on = date, study = student.study, name = student_name)
                    att.save()
                
            # Show successful upload message and display selected fields in the form
            # Disable submit button; enable and reset fields next day 
            return redirect('teacherhome:attendance')

        return render(request, self.template_name, {'form': form})

class SendAttendanceView(View):
    template_name = 'teacherhome/sendattendance.html'
    
    def get(self, request, *args, **kwargs):
        current_user = request.user    
        teacher = Teacher.objects.get(user = current_user) 
        
        template = get_template('teacherhome/sendattendance.html')
        bundle = dict()
        if teacher.is_class_teacher:    
            current_user = request.user
            # teacher = Teacher.objects.get(user = current_user)
            # students = Student.objects.filter(school = teacher.school,  study = teacher.class_teacher_of)
            
            
            
            absent_date = datetime.date.today()
            absent = Attendance.objects.filter(school = teacher.school, study = teacher.class_teacher_of, absent_on = absent_date)
            print(absent)
            key = 1
            for i in absent:
                bundle[key] = i.name
                key += 1 
            
            # html = template.render({'bundle': bundle})
            pdf = render_to_pdf('teacherhome/sendattendance.html', {'bundle': bundle})
            return HttpResponse(pdf, content_type='application/pdf')
            
            # return HttpResponse(html)

            # return render(request, self.template_name, {'bundle': bundle})
        else:
            return redirect('teacherhome:notallowed')

    def post(self, request):
        #yet to be completed
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

class NotClassTeacherView(View):
    template_name = 'teacherhome/notclassteacher.html'
    def get(self, request):
        return render(request, self.template_name)

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










