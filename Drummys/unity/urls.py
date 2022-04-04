from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/topscores', views.usertopscores, name='user/topscores'),
    path('user/level', views.level, name='user/level'),
]