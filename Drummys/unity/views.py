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
    stringSQL = '''SELECT Party.id, User.username, Countries.name as Country, 
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
            d["username"] = r[1]
            d["country"] = r[2]
            d["total_score"] = r[3]
            d["time_played"] = r[4]
            d["date_created"] = r[5]
            lista_salida.append(d)
        j = dumps(lista_salida)
    return HttpResponse(j, content_type="text/json-comment-filtered")

