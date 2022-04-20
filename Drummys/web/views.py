from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import loads,dumps
from django.http import Http404
import datetime
import sqlite3

# Create your views here.
def index(req):
    return render(req, 'web/index.html', ({}))

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


# ------ AUTH ---------
def authLogin(req):
    username = req.POST["username"]
    password = req.POST["password"]
    print('\n\n', username, password, '\n\n')

    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    # Find user with that username and password
    findUserSql = '''SELECT User.id, User.username, User.age, Countries.name, Countries.id, Countries.nickname 
    FROM User INNER JOIN Countries ON Countries.id=User.country_id WHERE User.username=? AND User.password=?'''
    # (id, username, password, age, countryName, countryId, countryNickname)
    user = cur.execute(findUserSql, (username, password)).fetchall()
    userId = user[0][0]
    userUsername = user[0][1]
    userAge = user[0][2]
    userCountryName = user[0][3]
    userCountryId = user[0][4]
    userCountryNickname = user[0][5]

    if (user is None):
        return Http404("No se encontró ese usuario")
    else:
        # If user exists create session and return session id
        dateCreated = datetime.datetime.now()
        createSessionSql = '''INSERT INTO Session (user_id, dateCreated) VALUES (?, ?)'''
        cur.execute(createSessionSql, (userId, dateCreated))
        retrieveSessionSql = '''SELECT id FROM Session WHERE user_id=? AND dateCreated=?;'''
        session = cur.execute(retrieveSessionSql, (str(userId), dateCreated)).fetchall()
        mydb.commit()
        json = dumps({
            "user": {
                "id": userId,
                "username": userUsername,
                "age": userAge,
                "countryId": userCountryId,
                "countryName": userCountryName,
                "countryNickname": userCountryNickname,
            },
            "session": {
                "id": session[0][0]
            }
        })
        return redirect('dashboard')


def authSignup(req):
    username = req.POST["username"]
    age = req.POST["age"]
    password = req.POST["password"]
    country = req.POST["country"]

    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''INSERT INTO User (username, country_id, password, age) VALUES (?, ?, ?, ?)'''
    cur.execute(stringSQL, (username, age, password, country,))
    retrieveUserSql = '''SELECT id FROM User WHERE username=? AND password=?'''
    user = cur.execute(retrieveUserSql, (username, password)).fetchall()
    mydb.commit()
    # return JsonResponse({"user": {"id": user[0][0]}})
    return redirect('login')


def updateUser(req):
    id = req.POST["id"]
    username = req.POST["username"]
    # User needs to be logged in -> missing logic

    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    updateUserSql = '''UPDATE User SET username = ? WHERE id=?;'''
    cur.execute(updateUserSql, (username, id))
    mydb.commit()

    return JsonResponse({"msg": 200})