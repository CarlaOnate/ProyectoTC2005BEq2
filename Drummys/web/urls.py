from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    #  --- VIEWS ---
    path('', views.index, name='index'),
    path('login', TemplateView.as_view(template_name='web/login.html'), name="login"),
    path('signup', TemplateView.as_view(template_name='web/signup.html'), name="signup"),
    path('dashboard', TemplateView.as_view(template_name='web/dashboard.html'), name="dashboard"),
    #  --- API ---
    path('stats', views.stats, name='stats'),
    path('visits', views.user_visits, name='user_visits'),
    path('downloads', views.downloads, name='downloads'),
    path('user/signup', views.authSignup, name='authSignup'),
    path('user/login', views.authLogin, name='authLogin'),
    path('user/updateUser', views.updateUser, name='updateUser'),
    path('topscores', views.topscores_global, name='topscores'),
    path('graficaL1', views.graficaL1, name='graficaL1'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('download', views.download, name='download'),
    path('download-logged', views.download_logged, name='download-logged'),
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('my-stats', views.my_stats, name='my-stats'),
    path('signup', views.signup, name='signup'),
    path('stats', views.stats, name='stats'),
    path('thankyou', views.thankyou, name='thankyou'),
]