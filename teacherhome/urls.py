from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'teacherhome'

urlpatterns = [
    url(r'^$', views.TeacherHomepageView.as_view(), name='teacher_homepage'),
    url(r'logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'add_assign/$', views.AddassignFormView.as_view(), name='add_assign'),
    url(r'attendance/$', views.ClassAttendanceView.as_view(), name='attendance'),

    url(r'sendattendance/$', views.SendAttendanceView.as_view(), name='sendattendance'),
    url(r'sendmessage/$', views.SendMessageView.as_view(), name='sendmessage'),
    url(r'sendresult/$', views.SendResultView.as_view(), name='sendresult'),

    
    url(r'notification/$', views.NotificationView.as_view(), name='notification'),
    url(r'schedule/$', views.ScheduleView.as_view(), name='schedule'),
]