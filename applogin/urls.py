from django.conf.urls import url
from . import views

app_name = 'applogin'

urlpatterns = [
    url(r'^$', views.LoginFormView.as_view(), name='login'),
    url(r'register/$', views.SchoolView.as_view(), name='register'),
    url(r'requestpwd/$', views.RequestpwdFormView.as_view(), name='requestpwd'),
    url(r'resetpwd/$', views.ResetpwdFormView.as_view(), name='resetpwd'),
]