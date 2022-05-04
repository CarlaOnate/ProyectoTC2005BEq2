from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    # --- AUTH  ---
    path('login', views.authLogin, name='game/authLogin'),
    # --- API ---
    path('party', views.game_party, name='game/party'),
    path('party2', views.game_party2, name='game/party2'),
    path('level', views.level, name='level'),
    path('logout', views.authLogout, name='game/authLogout')
]