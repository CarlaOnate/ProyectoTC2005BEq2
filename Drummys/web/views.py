from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import loads,dumps
from django.http import Http404
import datetime
import sqlite3
import collections

# Create your views here.
def index(request):
    return render(request, 'index.html')

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
            date = datetime.datetime.strptime(r[6], "%Y-%m-%d %H:%M:%S").strftime("%A %d. %b")
            d = [r[2], r[3], r[4], r[5], date]
            lista_salida.append(d)
        j = dumps(lista_salida)
    return j

def graficaGlobalLevel(level):
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
            d = [r[2], r[7]]
            lista_salida.append(d)
        j = dumps(lista_salida)

    title = 'Graph Level ' + str(level)
    modified_title = dumps(title)
    print('\n\nj =>', j ,'\n\n')
    return({
        'values': j,
        'title': modified_title
    })

def user_visits(req):
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
    return dataJson

def downloads(req):
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
    return dataJson

def stats(req):
    downloadJson = downloads(req)
    visitsJson = user_visits(req)
    topscoresGlobal = topscores_global(req)
    level1Global = graficaGlobalLevel(1)
    level2Global = graficaGlobalLevel(2)
    level3Global = graficaGlobalLevel(3)
    return render(req, 'web/stats.html', {
        "downloads": downloadJson,
        "visits": visitsJson,
        "topscores": topscoresGlobal,
        "level1": level1Global,
        "level2": level2Global,
        "level3": level3Global,
    })

# -- KINK OF STATIC VIEWS --
def aboutus(request):
    return render(request, 'aboutus.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def download(request):
    return render(request, 'download.html')

def download_logged(request):
    return render(request, 'download-logged.html')

def my_stats(request):
    return render(request, 'my-stats.html')

def thankyou(request):
    return render(request, 'thankyou.html')

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