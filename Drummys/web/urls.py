from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('visits', views.user_visits, name='user_visits'),
    path('downloads', views.downloads, name='downloads')
]