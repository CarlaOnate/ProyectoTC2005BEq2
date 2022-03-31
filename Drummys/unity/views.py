from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Countries

# Create your views here.


def index(req):
    return HttpResponse('<p>Soy Index</p>')

@csrf_exempt
def modelo(req):
    username = req.POST["username"]
    age = req.POST["age"]
    password = req.POST["password"]
    country = req.POST["country"]

    country = Countries.objects.get(nickname="MX")

    print('\n\ncountry_id =>', country.nickname, '\n\n')

    user = User(username=username, age=age, password=password, country_id=country)

    print('\n\nuser', user, '\n\n')

    user.save()

    return JsonResponse({"msg": 200})
