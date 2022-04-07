from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('topscores', views.topscores_global, name='/topscores'),
]