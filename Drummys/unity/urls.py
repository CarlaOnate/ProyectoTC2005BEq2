from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    # --- AUTH  ---
    path('game/login', views.login, name='user/login'),
    # --- API ---
    path('user/topscores', views.user_topscores, name='user/topscores'),
    path('user/level', views.user_level, name='user/level'),
    path('user/sessions', views.user_sessions, name='user/sessions'),
    path('game/party', views.game_party, name='game/party'),
    path('game/level', views.level, name='level')
]