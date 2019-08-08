from django.conf.urls import url
from . import views

app_name = 'applogin'

urlpatterns = [
    url(r'^$', views.LoginFormView.as_view(), name='login'),
    url(r'register/$', views.RegistrationFormView.as_view(), name='register'),
    url(r'registerSchool/$', views.SchoolFormView.as_view(), name='registerschool'),
    url(r'requestpwd/$', views.RequestpwdFormView.as_view(), name='requestpwd'),
    url(r'regsuccess/$', views.RegistrationSuccessView.as_view(), name='successful_reg'),
]