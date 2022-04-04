from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import loads,dumps
from django.http import Http404
import collections
import sqlite3
# Create your views here.

def index(req):
    return HttpResponse('<p>Soy Index</p>')

def usertopscores(request):
    usuario = request.GET['user_id']
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''SELECT Party.id, User.id as User_ID, User.username, Countries.name as Country, 
Party.total_score, Party.time_played, Party.dateCreated FROM  Party
 INNER JOIN User, Countries ON Party.user_id = User.id  AND Countries.id = User.country_id WHERE Party.user_id = ? 
 ORDER BY Party.total_score LIMIT 10 '''
    rows = cur.execute(stringSQL, (str(usuario),))
    if rows is None:
        raise Http404("user_id does not exist")
    else:
        lista_salida = []
        for r in rows:
            print(r)
            d = {}
            d["party_id"] = r[0]
            d["user_id"] = r[1]
            d["username"] = r[2]
            d["country"] = r[3]
            d["total_score"] = r[4]
            d["time_played"] = r[5]
            d["date_created"] = r[6]
            lista_salida.append(d)
        j = dumps(lista_salida)
    return HttpResponse(j, content_type="text/json-comment-filtered")

def level(request):
    usuario = request.GET['user_id']
    level = request.GET['level']
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''SELECT Levels.id as Lvl_ID, User.id as User_ID,User.username, Countries.name as Country, 
Party.id as Party_id, Levels.difficulty as level, Levels.played_audio,  Levels.final_time, Levels.penalties, Levels.dateCreated 
FROM  Levels INNER JOIN User, Countries, Party ON Levels.user_id = User.id  AND Party.id=Levels.party_id AND 
Countries.id = User.country_id WHERE Levels.user_id = ?  AND Levels.difficulty= ? ORDER BY Levels.final_time  
LIMIT 10'''
    rows = cur.execute(stringSQL, (usuario, level, ))
    if rows is None:
        raise Http404("user_id does not exist")
    else:
        lista_salida = []
        for r in rows:
            print(r)
            d = {}
            d["level_id"] = r[0]
            d["user_id"] = r[1]
            d["username"] = r[2]
            d["country"] = r[3]
            d["difficulty"] = r[4]
            d["played_audio"] = r[5]
            d["final_time"] = r[6]
            d["penalties"] = r[7]
            d["dateCreated"] = r[8]
            lista_salida.append(d)
        j = dumps(lista_salida)
    return HttpResponse(j, content_type="text/json-comment-filtered")

