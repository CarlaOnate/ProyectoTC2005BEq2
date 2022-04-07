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
    return render(req, 'web/index.html', ({"valor": 111}))


def topscores_global(request):
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''SELECT Party.id, User.id as User_ID, User.username, Countries.nickname as Country, 
Party.total_score, Party.time_played, Party.dateCreated FROM  Party
 INNER JOIN User, Countries ON Party.user_id = User.id  AND Countries.id = User.country_id 
 ORDER BY Party.total_score LIMIT 10 '''
    rows = cur.execute(stringSQL)
    if rows is None:
        raise Http404("user_id does not exist")
    else:
        lista_salida = [["Username", "Country", "Total Score", "Time Played", "Date"]]
        for r in rows:
            print(r)
            d = [r[2], r[3], r[4], r[5], r[6]]
            lista_salida.append(d)
        j = dumps(lista_salida)

    title = 'Global Top Scores'
    modified_title = dumps(title)

    return render(request, 'tablaTopScores.html', {'values': j, 'title': modified_title})

def graficaL1(request):
    level = request.GET['level']
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''SELECT Levels.id as Lvl_ID, User.id as User_ID,User.username, Countries.name as Country, 
Party.id as Party_id, Levels.difficulty as level, Levels.played_audio,  Levels.final_time, Levels.penalties, 
Levels.dateCreated 
FROM  Levels INNER JOIN User, Countries, Party ON Levels.user_id = User.id  AND Party.id=Levels.party_id AND 
Countries.id = User.country_id WHERE Levels.difficulty= ? ORDER BY Levels.final_time  
LIMIT 10'''
    rows = cur.execute(stringSQL, (level,))
    if rows is None:
        raise Http404("user_id or level does not exist")
    else:
        lista_salida = [['Users', 'Time (s)']]
        for r in rows:
            print(r)
            d = [r[2], r[7]]
            lista_salida.append(d)
        j = dumps(lista_salida)

    title = 'Graph Level 1'
    modified_title = dumps(title)

    return render(request, 'barrasHorizontales.html', {'values': j, 'title': modified_title})

