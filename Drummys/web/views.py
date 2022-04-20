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
    stringSQL = '''select count (*), dateCreated from Visit where dateCreated = Visit.dateCreated group by dateCreated LIMIT 10;'''
    rows = cur.execute(stringSQL)
    if rows is None:
        raise Http404("List not available")
    else:
        data = [['Date', 'Visits']]
        for r in rows:
            date = datetime.datetime.strptime(r[1], "%Y-%m-%d %H:%M:%S").strftime("%A %d. %b")
            data.append([date, r[0]])
        dataJson = dumps(data)
    return render(request, 'web/visits.html', {'data': dataJson})

def downloads(request):
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''SELECT COUNT(*), Countries.name FROM Download INNER JOIN  User, Countries ON Download.user_id = User.id
    AND Countries.id = User.country_id GROUP BY Countries.name'''
    rows = cur.execute(stringSQL)
    if rows is None:
        raise Http404("List not available")
    else:
        data = [['Country', 'Downloads']]
        for r in rows:
            data.append([r[1], r[0]])
        dataJson = dumps(data)
        print(data)
    return render(request, 'web/download-graph.html', {'data': dataJson})

def stats(req):
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()

    downloadsSql = '''SELECT COUNT(*), Countries.name FROM Download INNER JOIN  User, Countries ON Download.user_id = User.id
    AND Countries.id = User.country_id GROUP BY Countries.name'''
    visitsSql = '''select count (*), dateCreated from Visit where dateCreated = Visit.dateCreated group by dateCreated LIMIT 10;'''

    downloads = cur.execute(downloadsSql).fetchall()
    visits = cur.execute(visitsSql).fetchall()

    dataDownload = [['Country', 'Downloads']]
    dataVisits = [['Date', 'Visits']]
    for el in downloads:
        dataDownload.append([el[1], el[0]])

    for el in visits:
        date = datetime.datetime.strptime(el[1], "%Y-%m-%d %H:%M:%S").strftime("%A %d. %b")
        dataVisits.append([date, el[0]])

    downloadJson = dumps(dataDownload)
    visitsJson = dumps(dataVisits)
    print('\n\ndataVisits', dataVisits)
    print('\n\ndataDownload', dataDownload)
    return render(req, 'web/stats.html', {"download": downloadJson, "visits": visitsJson})

