from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

#PDFTemplateView
from wkhtmltopdf.views import PDFTemplateView

app_name = 'teacherhome'

urlpatterns = [
    url(r'^$', views.TeacherhomepageView.as_view(), name='teacher_homepage'),
    url(r'logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'add_assign/$', views.AddassignFormView.as_view(), name='add_assign'),

    url(r'view_assign/$', views.AssignmentView.as_view(), name='view_assign'),
    path('seeassign/<slug:path>/', views.SeeAssignmentView.as_view(), name='seeassign'),


    url(r'sendattendance/$', views.SendAttendanceView.as_view(), name='absentmsg'),
    url(r'attendance/$', views.AttendanceFormView.as_view(), name='attendance'),
    url(r'studentattendanceform/$', views.AttendanceviewFormView.as_view(), name='studentattendanceform'),

    url(r'announcement/$', views.AnnouncementView.as_view(), name='announcement'),
    path('announcement/<slug:announcement>/', views.AnnouncementDetailView.as_view(), name='announcement_detail'),

    # url(r'teachersubject/$', views.MarksView.as_view(), name='teachersubject'),
    # url(r'teachersubject/<slug:study>/$', views.MarksAddView.as_view(), name='subject'),

    url(r'notallowed/$', views.NotClassTeacherView.as_view(), name='notallowed'),
    
    url(r'sendresult/$', views.SendResultView.as_view(), name='sendresult'),
    url(r'notification/$', views.NotificationView.as_view(), name='notification'),
    url(r'schedule/$', views.ScheduleView.as_view(), name='schedule'),
    
    url(r'#', views.TeacherUpdateView.as_view(), name='teacher_update'),
]