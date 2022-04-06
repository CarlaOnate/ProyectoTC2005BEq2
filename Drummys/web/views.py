from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def index(req):
    return render(req, 'web/index.html', ({"valor": 111}))