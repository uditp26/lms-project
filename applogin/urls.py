from django.conf.urls import url
from . import views

app_name = 'applogin'

urlpatterns = [
    url(r'^$', views.LoginFormView.as_view(), name='login'),
    url(r'user/add/$', views.UserCreate.as_view(), name='user_add'),
]