from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'adminhome'

urlpatterns = [
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'students/$', views.StudentView.as_view(), name='students'),
    url(r'teachers/$', views.TeacherView.as_view(), name='teachers'),
    url(r'principal/$', views.PrincipalView.as_view(), name='principal'),
    url(r'students/addstudent/$', views.AddstudentFormView.as_view(), name='addstudent'),
    url(r'teachers/addteacher/$', views.AddteacherFormView.as_view(), name='addteacher'),
]