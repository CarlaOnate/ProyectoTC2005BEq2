from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import sqlite3

# Create your views here.
def index(req):
    return HttpResponse('<p>Soy Index</p>')

@csrf_exempt
def signup(req):
    username = req.POST["username"]
    age = req.POST["age"]
    password = req.POST["password"]
    country = req.POST["country"]

    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''INSERT INTO User (username, country_id, password, age) VALUES (?, ?, ?, ?)'''
    # cur.execute(stringSQL, (username, age, password, country,))
    cur.execute(stringSQL)

    return JsonResponse({"msg": 200})