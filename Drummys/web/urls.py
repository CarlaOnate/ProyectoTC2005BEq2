from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    #  --- VIEWS ---
    path('', views.index, name='index'),
    path('login', TemplateView.as_view(template_name='web/login.html'), name="login"),
    path('signup', views.signup, name='signup'),
    path('dashboard', TemplateView.as_view(template_name='web/dashboard.html'), name="dashboard"),
    path('aboutus', views.aboutus, name='aboutus'),
    path('download', views.download, name='download'),
    path('download-logged', views.download_logged, name='download-logged'),
    path('my-stats', views.myStats, name='myStats'),
    path('thankyou', views.thankyou, name='thankyou'),
    path('stats', views.stats, name='stats'),
    path('profile', views.profile, name='profile'),
    #  --- API ---
    path('api/download', views.addDownload, name='addDownload'),
    path('user/signup', views.authSignup, name='authSignup'),
    path('user/login', views.authLogin, name='authLogin'),
    path('user/updateUser', views.updateUser, name='updateUser'),
    path('user/getUser', views.getUser, name='getUser'),
    path('user/logout', views.authLogout, name='authLogout'),
]