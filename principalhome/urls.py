from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'principalhome'

urlpatterns = [
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'students/$', views.StudentView.as_view(), name='students'),
    path('students/<slug:clss>/', views.StudentIndexView.as_view(), name='class_students'),
    path('students/<slug:clss>/<slug:student>/', views.StudentDetailView.as_view(), name='students_detail'),
    url(r'teachers/$', views.TeacherView.as_view(), name='teachers'),
    path('teachers/<slug:teacher>/', views.TeacherDetailView.as_view(), name='teachers_detail'),
    url(r'announcements/$', views.AnnouncementView.as_view(), name='announcements'),
    url(r'makeAnnouncement/$', views.AnnouncementFormView.as_view(), name='announce'),
]