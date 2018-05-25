from django.conf.urls import url
from . import views


app_name = 'users'
urlpatterns = [
    url(r'^login/$', views.Login, name="login"),
    url(r'^logout/$', views.Logout, name="logout"),
    url(r'^register/$', views.Register, name="register"),
    url(r'^reset/$', views.Reset, name="reset"),
    url(r'^forget_email/$', views.ForgetEmail, name="forget_email"),
    # url(r'^forget_confirm/$', views.ForgetConfirm, name='forget_confirm'),
    url(r'^forget_done/$', views.ForgetDone, name='forget_done'),
]
