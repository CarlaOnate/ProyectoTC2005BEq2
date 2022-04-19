from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #POST
    path('user/signup', views.signup, name='signup'),
    path('user/login', views.login, name='login'),
    path('user/updateUser', views.updateUser, name='updateUser'),
    path('game/alta', views.alta, name='alta'),
    path('level', views.level, name='level'),
    path('cambio', views.cambio, name='cambio'),
    path('consulta', views.consulta, name='consulta')
]