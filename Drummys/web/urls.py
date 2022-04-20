from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stats', views.stats, name='stats'),
    path('visits', views.user_visits, name='user_visits'),
    path('downloads', views.downloads, name='downloads'),
    path('login', views.loginView, name='loginView'),
    path('user/login', views.authLogin, name='authLogin'),
]