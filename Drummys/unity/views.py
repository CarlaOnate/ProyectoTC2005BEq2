from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def index(req):
    return HttpResponse('<p>Soy Index</p>')