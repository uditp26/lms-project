from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'studenthome'

urlpatterns = [
    url(r'^$', views.TeacherhomepageView.as_view(), name='studenthome'),
    url(r'logout/$', views.LogoutView.as_view(), name='logout'),
   
    url(r'allassignment/$', views.AssignmentView.as_view(), name='allassignment'),
    url(r'currentassignment/$', views.CurrentassignmentView.as_view(), name='currentassignment'),
    path('seeassign/<slug:path>/', views.SeeAssignmentView.as_view(), name='seeassign'), 

    url(r'view_marks/$', views.MarksView.as_view(), name='view_marks'),
    path('seemarks/<slug:path>/', views.SeeMarksView.as_view(), name='seemarks'),
    
    url(r'announcement/$', views.AnnouncementView.as_view(), name='announcement'),
    path('announcement/<slug:announcement>/', views.AnnouncementDetailView.as_view(), name='announcement_detail'),
    
    url(r'attendance/$', views.AttendanceView.as_view(), name='attendance'),
]
