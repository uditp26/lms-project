from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'studenthome'

urlpatterns = [
    url(r'^$', views.TeacherhomepageView.as_view(), name='studenthome'),
    url(r'logout/$', views.LogoutView.as_view(), name='logout'),
   
    url(r'allassignment/$', views.AssignmentView.as_view(), name='allassignment'),
    url(r'currentassignment/$', views.CurrentassignmentView.as_view(), name='currentassignment'),
    
    url(r'attendance/$', views.AttendanceView.as_view(), name='attendance'),
]
