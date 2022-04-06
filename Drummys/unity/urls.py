from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/topscores', views.user_topscores, name='user/topscores'),
    path('user/level', views.user_level, name='user/level'),
    path('user/sessions', views.user_sessions, name='user/sessions'),
    path('visits', views.user_visits, name='user/visits'),
    path('downloads', views.downloads, name='downloads'),
    path('game/party', views.game_party, name='game/party'),
    path('prueba', views.prueba, name='prueba'),
]