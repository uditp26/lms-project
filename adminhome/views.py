from django.shortcuts import render, reverse, render
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from .models import LocalAdmin, Student, Teacher, Principal, Parent
from .forms import AddstudentForm, AddteacherForm

class HomepageView(View):
    template_name = 'adminhome/homepage.html'
    # context = {'admin': LocalAdmin.objects.get(pk=1)} # use filter()

    def get(self, request):
        current_user = request.user
        return render(request, self.template_name, {'admin': current_user})

class StudentView(View):
    template_name = 'adminhome/students.html'

    def get(self, request):
        return render(request, self.template_name)

class AddstudentFormView(View):
    form_class = AddstudentForm
    template_name = 'adminhome/addstudent_form.html'

    # displays a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            pass

        return render(request, self.template_name, {'form': form})

class StudentIndexView(generic.ListView):
    template_name = 'adminhome/students_index.html'

    def get_queryset(self):
        return Student.objects.all()

class TeacherView(View):
    template_name = 'adminhome/teachers.html'

    def get(self, request):
        return render(request, self.template_name)

class AddteacherFormView(View):
    form_class = AddteacherForm
    template_name = 'adminhome/addteacher_form.html'

    # displays a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            pass

        return render(request, self.template_name, {'form': form})

class PrincipalView(View):
    template_name = 'adminhome/principal.html'

    def get(self, request):
        return render(request, self.template_name) 

class LogoutView(View):
    template_name = 'applogin/login.html'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('applogin:login'))
