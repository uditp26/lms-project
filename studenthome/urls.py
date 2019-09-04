from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'adminhome'

urlpatterns = [
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    # url(r'logout/$', views.AttendanceView.as_view(), name='attendance'),
    # url(r'students/$', views.AssignmentView.as_view(), name='fullassignment'),
    # url(r'teachers/$', views.CurrentassignmentView.as_view(), name='currentassignment'),

]
