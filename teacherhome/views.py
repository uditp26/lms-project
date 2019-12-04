from django.shortcuts import render, reverse, redirect
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from .models import Assignment, Attendance, Marksdetails
from .forms import AddassignForm, AttendanceForm, AttendanceviewForm, AddmarksForm

from adminhome.models import School, Student, Teacher
from principalhome.models import Announcement

from collections import defaultdict
from django.urls import reverse_lazy
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import datetime
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

#show pdf
from django.contrib import messages
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings

#html to pdf 
# pip install --pre xhtml2pdf
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

decorators = [cache_control(no_cache=True, must_revalidate=True, no_store=True), login_required(login_url='http:/127.0.0.1:8000/applogin/')]
                                         
@method_decorator(decorators, name='dispatch')
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


@method_decorator(decorators, name='dispatch')
class AddmarksFormView(View):
    form_class = AddmarksForm
    template_name = 'teacherhome/addmarks_form.html'

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
            addmarks = form.save(commit = False)
            addmarks.teacher =  teacher
            student = Student.objects.get(study = teacher.class_teacher_of, school = teacher.school, roll_no = addmarks.roll_no)
            addmarks.name  = str(student.first_name) +' '+ str(student.last_name)
            addmarks.save()

            return redirect('teacherhome:view_marks')
        return render(request, self.template_name, {'form': form})  

class MarksView(View):
    template_name = 'teacherhome/marks_view.html'

    def get(self, request):
        current_user = request.user
        teacher = Teacher.objects.get(user = current_user)  
        marksheets = Marksdetails.objects.filter(teacher = teacher)

        bundle = dict()
        key = 1
        for a in marksheets:
            bundle[key] = a
            key += 1 
        return render(request, self.template_name, {'marksheets': bundle})

class SeeMarksView(View):
    template_name = 'teacherhome/marks_see.html'
    def get(self, request, path):
        filename =str(path).split('_')
        filename1 = []
        for i in range(3,len(filename)):
            filename1.append(filename[i])
        filename2 = ''
        for i in range(len(filename1)):
            filename2 += filename1[i]
            if i+1 < len(filename1):
                filename2 += '_'
        rel_path = 'media/'+str(filename[0])+'/'+str(filename[1])+"_"+str(filename[2])+'/'+str(filename2)+".pdf"
        return FileResponse(open(rel_path, 'rb'), content_type='application/pdf')

@method_decorator(decorators, name='dispatch')
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
            addassign.school = teacher.school
            addassign.save() 
            return redirect('teacherhome:view_assign')
        return render(request, self.template_name, {'form': form})  

class SeeAssignmentView(View):
    template_name = 'teacherhome/assignment_see.html'
    def get(self, request, path):
        filename =str(path).split('_')
        filename1 = []
        for i in range(3,len(filename)):
            filename1.append(filename[i])
        filename2 = ''
        for i in range(len(filename1)):
            filename2 += filename1[i]
            if i+1 < len(filename1):
                filename2 += '_'
        rel_path = 'media/'+str(filename[0])+'/'+str(filename[1])+"_"+str(filename[2])+'/'+str(filename2)+".pdf"
        return FileResponse(open(rel_path, 'rb'), content_type='application/pdf')

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

@method_decorator(decorators, name='dispatch')
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

#enter roll number and generate pdf for how many days studnet absent
@method_decorator(decorators, name='dispatch')
class ShowAttendanceView(View):
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
            
            #edit from here.......................

            absent_date = datetime.date.today()
            absent = Attendance.objects.filter(school = teacher.school, study = teacher.class_teacher_of, absent_on = absent_date)
            
            # roll_number = []
            # for i  in all_absent:
            #     if i.roll_no not in roll_number:
            #         roll_number.append(i.roll_no)

            key = 1
            for i in absent:
                bundle[key] = i
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


@method_decorator(decorators, name='dispatch')
class AttendanceviewFormView(View):
    form_class = AttendanceviewForm
    template_name = 'teacherhome/studentattendance_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        current_user = request.user
        teacher = Teacher.objects.get(user = current_user) 
        bundle = dict()
        if form.is_valid():
            roll_no = form.cleaned_data['roll_no']
            try:
                absent = Attendance.objects.filter(roll_no = roll_no, school = teacher.school, study = teacher.class_teacher_of)
            except:
                form.add_error('roll_no', "Roll number does not exist in your class.")

            key = 1
            for i in absent:
                bundle[key] = i
                key += 1 
            
            pdf = render_to_pdf('teacherhome/sendattendance.html', {'bundle': bundle})
            return HttpResponse(pdf, content_type='application/pdf')

        return render(request, self.template_name, {'form': form})


@method_decorator(decorators, name='dispatch')
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

            key = 1
            for i in absent:
                bundle[key] = i
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

# Dont delete below code
# @method_decorator(decorators, name='dispatch')
# class MarksView(View):
#     template_name = 'teacherhome/marks.html'
    
#     def get(self, request):
#         current_user = request.user    
#         teacher = Teacher.objects.get(user = current_user) 
#         study = teacher.class_teacher_of
#         subject = teacher.subject
#         teacher_subject = dict()
#         teacher_subject[study] = subject
#         return render(request, self.template_name, {'teacher_subject': teacher_subject})

# @method_decorator(decorators, name='dispatch')
# class MarksAddView(View):
#     template_name = 'teacherhome/marksadd.html'

#     def get(self, request, studysubject):
#         current_user = request.user    
#         teacher = Teacher.objects.get(user = current_user) 
#         students = Student.objects.filter(school = teacher.school , study = teacher.class_teacher_of)
#         marks_details = Marksdetails()
#         for s in  students:
#             marks_details.name = s.first_name+ ' '+s.last_name 
#             marks_details.roll_no = s.roll_no
#             marks_details.study = s.study
#             marks_details.school = s.school

#         marks_details.save()
#         return render(request, self.template_name, {'marks_details': marks_details})
        
# Add marks form
# class MarksDetailsFormView(View):
#     template_name = 'teacherhome/marks_details.html'
    
#     def get(self, request):        
#         current_user = request.user
#         teacher = Teacher.objects.get(user = current_user)
#         students = Student.objects.filter(school = techer.school , study = teacher.class_teacher_of)

#         return render(request, self.template_name, {'students': students})

# class MarksDetailsView(View):
#     template_name = 'teacherhome/marks_details-form.html'

#     def get(self, request):
#         current_user = request.user    
#         teacher = Teacher.objects.get(user = current_user) 
#         students = Student.objects.filter(school = techer.school , study = teacher.class_teacher_of)
#         return render(request, self.template_name, {'teacher': teacher})


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


#                                                               ANNOUNCEMENT

@method_decorator(decorators, name='dispatch')
class AnnouncementView(View):
    template_name = 'teacherhome/announcements.html'

    def get(self, request):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            # student = Student.objects.get(user = current_user)
            current_date = datetime.date.today()
            announcement_type1 = Announcement.objects.filter(audience="Teachers", expiry_date__gte = current_date)
            announcement_type2 = Announcement.objects.filter(audience="All", expiry_date__gte = current_date)
            
            announcements = announcement_type1 | announcement_type2

            return render(request, self.template_name, {'announcements': announcements})

@method_decorator(decorators, name='dispatch')
class AnnouncementDetailView(View):
    template_name = 'teacherhome/announcement_detail.html'

    def get(self, request, announcement):
        current_user = request.user
        if str(current_user) is 'AnonymousUser':
            raise Http404
        else:
            school = request.user.school
            principal = Principal.objects.get(school = school)
           
            announcement1 = Announcement.objects.get(announcer = principal, audience="Teachers")
            announcement2 = Announcement.objects.get(announcer = principal, audience="All")
            announcement = announcement1 | announcement2

            return render(request, self.template_name, {'announcement': announcement})


@method_decorator(decorators, name='dispatch')
class NotClassTeacherView(View):
    template_name = 'teacherhome/notclassteacher.html'
    def get(self, request):
        return render(request, self.template_name)

@method_decorator(decorators, name='dispatch')
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

@method_decorator(decorators, name='dispatch')
class LogoutView(View):
    template_name = 'applogin/login.html'
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('applogin:login'))

class TeacherUpdateView(UpdateView):
    model = Teacher
    fields = ['first_name', 'last_name', 'date_of_birth', 'joining_date', 'email', 'phone', 'is_class_teacher', 'subject', 'resume']

