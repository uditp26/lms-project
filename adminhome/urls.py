from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'adminhome'
# prefix = '<slug:username>/'

urlpatterns = [
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    # path(prefix, views.HomepageView.as_view(), name='homepage'),
    url(r'registerSchool/$', views.RegisterschoolFormView.as_view(), name='registerSchool'),
    url(r'students/$', views.StudentView.as_view(), name='students'),
    url(r'students/addstudent/$', views.AddstudentFormView.as_view(), name='addstudent'),
    path('students/<slug:clss>/', views.StudentIndexView.as_view(), name='class_students'),
    path('students/<slug:clss>/<slug:enrolment_no>/', views.StudentDetailView.as_view(), name='students_detail'),
    url(r'teachers/$', views.TeacherView.as_view(), name='teachers'),
    url(r'teachers/addteacher/$', views.AddteacherFormView.as_view(), name='addteacher'),
    path('teachers/<slug:username>/', views.TeacherDetailView.as_view(), name='teachers_detail'),
    url(r'principal/$', views.PrincipalView.as_view(), name='principal'),
    url(r'principal/addPrincipal/$', views.AddprincipalFormView.as_view(), name='addPrincipal'),

]