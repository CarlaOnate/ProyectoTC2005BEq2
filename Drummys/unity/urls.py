from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #POST
    path('user/signup', views.signup, name='signup')
]