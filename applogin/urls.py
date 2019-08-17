from django.conf.urls import url, include
from . import views

app_name = 'applogin'

urlpatterns = [
    url(r'^$', views.LoginFormView.as_view(), name='login'),
    url(r'register/$', views.RegistrationFormView.as_view(), name='register'),
    url(r'requestpwd/$', views.RequestpwdFormView.as_view(), name='requestpwd'),
    url(r'resetpwd/$', views.ResetpwdFormView.as_view(), name='resetpwd'),
    url(r'regsuccess/$', views.RegistrationSuccessView.as_view(), name='successful_reg'),
    url(r'pwdchngsuccess/$', views.PwdChangeSuccessView.as_view(), name='successful_pwd'),
]