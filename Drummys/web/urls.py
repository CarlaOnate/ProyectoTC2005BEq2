from django.urls import path
from . import views

urlpatterns = [
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