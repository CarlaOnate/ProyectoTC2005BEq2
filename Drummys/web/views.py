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

def user_visits(request):
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''SELECT Visit.id, Visit.ip, Visit.device, Visit.dateCreated FROM Visit LIMIT 10'''
    rows = cur.execute(stringSQL)
    '''
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
            print(j)
    '''
    if rows is None:
        raise Http404("List not available")
    else:
        data = []
        for r in rows:
            print(r)
            d = {}
            d["visit_id"] = r[0]
            d["ip"] = r[1]
            d["device"] = r[2]
            d["dateCreated"] = r[3]
            data.append(d)
        j = dumps(data)
        print(j)
    #return HttpResponse(j, content_type="text/json-comment-filtered")
    return render(request, 'web/visits.html', { "data": data })