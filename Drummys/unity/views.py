from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import loads,dumps
from django.http import Http404
import datetime
import collections
import sqlite3
# Create your views here.

def index(req):
    return HttpResponse('<p>Soy Index</p>')

def user_topscores(request):
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

def user_level(request):
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
        raise Http404("user_id or level does not exist")
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


def user_sessions(request):
    usuario = request.GET['user_id']
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''SELECT Session.id as Session_id, Session.user_id, Session.time_played, Session.dateCreated FROM  Session
  WHERE Session.user_id = ?  ORDER BY Session.time_played  LIMIT 10'''
    rows = cur.execute(stringSQL, (usuario,))
    if rows is None:
        raise Http404("user_id does not exist")
    else:
        lista_salida = []
        for r in rows:
            print(r)
            d = {}
            d["session_id"] = r[0]
            d["user_id"] = r[1]
            d["time_played"] = r[2]
            d["dateCreated"] = r[3]
            lista_salida.append(d)
        j = dumps(lista_salida)
    return HttpResponse(j, content_type="text/json-comment-filtered")

def user_visits(request):
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''SELECT Visit.id, Visit.ip, Visit.device, Visit.dateCreated FROM Visit LIMIT 10'''
    rows = cur.execute(stringSQL)
    if rows is None:
        raise Http404("List not available")
    else:
        lista_salida = []
        for r in rows:
            print(r)
            d = {}
            d["visit_id"] = r[0]
            d["ip"] = r[1]
            d["device"] = r[2]
            d["dateCreated"] = r[3]
            lista_salida.append(d)
        j = dumps(lista_salida)
    return HttpResponse(j, content_type="text/json-comment-filtered")


def downloads(request):
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''SELECT Download.id as download_id, Download.user_id as user_id, Countries.name, 
    Download.device, Download.dateCreated FROM Download INNER JOIN  User, Countries ON Download.user_id = User.id 
    AND Countries.id = User.country_id'''
    rows = cur.execute(stringSQL)
    if rows is None:
        raise Http404("List not available")
    else:
        lista_salida = []
        for r in rows:
            print(r)
            d = {}
            d["download_id"] = r[0]
            d["user_id"] = r[1]
            d["country"] = r[2]
            d["device"] = r[3]
            d["dateCreated"] = r[4]
            lista_salida.append(d)
        j = dumps(lista_salida)
    return HttpResponse(j, content_type="text/json-comment-filtered")

@csrf_exempt
def game_party(request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)

    user_id = body['user_id']
    party_id = body['party_id']
    total_score = body['total_score']
    time_played = body['time_played']
    dateCreated = datetime.datetime.now()

    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()

    stringSQL = '''SELECT Party.session_id FROM Party WHERE Party.id = ?'''
    rows = cur.execute(stringSQL, (party_id, ))
    r = rows.fetchone()
    if rows is None:
        raise Http404("Party id does not exist")
    else:
        session_id = r[0]

    stringSQL = '''INSERT INTO "main"."Party" ( "user_id", "session_id", 
    "total_score", "time_played", "dateCreated") 
    VALUES (?, ?, ?, ?, ?);'''

    rows = cur.execute(stringSQL, (user_id, session_id, total_score, time_played, dateCreated, ))
    mydb.commit()

    if rows is None:
        raise Http404("It was not possible to register party data")
    else:
        d = {"msg": "200"}
        j = dumps(d)

    mydb.close()
    return HttpResponse(j, content_type="text/json-comment-filtered")
