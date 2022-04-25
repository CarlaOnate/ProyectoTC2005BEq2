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
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    dateCreated = datetime.datetime.now().replace(microsecond=0)
    ip = request.META.get('HTTP_HOST')
    device = request.META.get('HTTP_USER_AGENT')
    stringSQL = '''INSERT INTO Visit (ip, device, dateCreated) VALUES(?, ?, ?)'''
    cur.execute(stringSQL, (ip, device, dateCreated))
    mydb.commit()
    mydb.close()
    return render(request, 'web/index.html')

#  --- GRAPHS ---
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
    mydb.close()
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
    mydb.close()
    return({
        'values': j,
        'title': modified_title
    })

def user_level(level, usuario):
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
        lista_salida = [['Date', 'Time (s)']]
        for r in rows:
            date = datetime.datetime.strptime(r[9], "%Y-%m-%d %H:%M:%S").strftime("%A %d. %b")
            d = [date, r[7]]
            lista_salida.append(d)
        j = dumps(lista_salida)
    title = 'Graph Level ' + str(level)
    modified_title = dumps(title)
    mydb.close()
    return({
        'values': j,
        'title': modified_title
    })

def user_sessions(usuario):
    # usuario = request.GET['user_id']
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''SELECT SUM(time_played) AS total, date FROM Session WHERE Session.user_id = ?
    Group by date Order by time_played asc'''
    rows = cur.execute(stringSQL, (usuario,))
    if rows is None:
        raise Http404("user_id does not exist")
    else:
        lista_salida = [['Date', 'Time (s)']]
        for r in rows:
            date = datetime.datetime.strptime(r[1], "%Y-%m-%d").strftime("%A %d. %b")
            d = [date, r[0]]
            lista_salida.append(d)
        j = dumps(lista_salida)
    mydb.close()
    return j

def user_topscores(usuario):
    # usuario = request.GET['user_id']
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
        lista_salida = [["Username", "Country", "Total Score", "Time Played", "Date"]]
        for r in rows:
            print('\n\n date =>', r[6])
            date = datetime.datetime.strptime(r[6], "%Y-%m-%d %H:%M:%S").strftime("%A %d. %b")
            d = [r[2], r[3], r[4], r[5], date]
            lista_salida.append(d)
        j = dumps(lista_salida)
    mydb.close()
    return j

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
    mydb.close()
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
    mydb.close()
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

def myStats(req):
    topscores = user_topscores(1) # seria pasar el req.user
    sessions = user_sessions(1) # seria pasar el req.user
    level1 = user_level(1, 1) # seria pasar el req.user
    level2 = user_level(2, 1) # seria pasar el req.user
    level3 = user_level(3, 1) # seria pasar el req.user
    print('\n\n topscores =>', topscores, '\n\n')
    print('\n\n sessions =>', sessions, '\n\n')
    print('\n\n level =>', level1, '\n\n')
    return render(req, 'web/my-stats.html', {
        "topscores": topscores,
        "sessions": sessions,
        "level1": level1,
        "level2": level2,
        "level3": level3,
    })

# -- KINK OF STATIC VIEWS --
def aboutus(request):
    return render(request, 'web/aboutus.html')

def dashboard(request):
    return render(request, 'web/dashboard.html')

def download(request):
    return render(request, 'web/download.html')

def download_logged(request):
    return render(request, 'web/download-logged.html')

def thankyou(request):
    return render(request, 'web/thankyou.html')

def login(request):
    return render(request, 'web/login.html')

def signup(req):
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()

    findUserSql = '''SELECT * From Countries'''
    countries = cur.execute(findUserSql).fetchall()
    countriesArr = []
    for el in countries:
        countriesArr.append(el[2])
    countriesJson = dumps(countriesArr)
    mydb.close()
    return render(req, 'web/signup.html', {"countries": countriesJson})

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

    mydb.close()

    if (user is None):
        return Http404("No se encontró ese usuario")
    else:
        # If user exists create session and return session id
        dateCreated = datetime.datetime.now().replace(microsecond=0)
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

    countrySql = '''SELECT id FROM Countries WHERE name=?;'''
    countryId = cur.execute(countrySql, (country,)).fetchall()

    stringSQL = '''INSERT INTO User (username, country_id, password, age) VALUES (?, ?, ?, ?)'''
    cur.execute(stringSQL, (username,  countryId[0][0], password, age))
    retrieveUserSql = '''SELECT id FROM User WHERE username=? AND password=?'''
    user = cur.execute(retrieveUserSql, (username, password)).fetchall()
    mydb.commit()
    mydb.close()
    return redirect('thankyou')

# @login_required # todo
def updateUser(req):
    # id = req.POST["id"] # todo: se saca de req.user
    id = "1"
    username = req.POST["username"]
    # User needs to be logged in -> missing logic

    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    updateUserSql = '''UPDATE User SET username = ? WHERE id=?;'''
    cur.execute(updateUserSql, (username, id))
    mydb.commit()
    mydb.close()

    return JsonResponse({"msg": 200})

# @login_required # todo
def getUser(req):
    # id = req.POST["id"] # todo: se saca de req.user
    id = "1"

    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    getUserSql = '''SELECT User.id, User.username, Countries.name as Country, User.age FROM User
    , Countries WHERE User.id = ? AND Countries.id = User.country_id;'''
    user = cur.execute(getUserSql, (id)).fetchall()
    mydb.commit()
    mydb.close()

    return JsonResponse({"id": user[0][0], "username": user[0][1], "country": user[0][2], "age": user[0][3]})

# @login_required # todo
def authLogout(req):
    id = "1" # todo: se sacaría de req.user
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()

    retrieveSessionSql = '''SELECT id, dateCreated FROM Session WHERE user_id=? AND date IS NULL AND time_played IS NULL;'''
    session = cur.execute(retrieveSessionSql, (id)).fetchall()

    date = datetime.datetime.now().replace(microsecond=0)
    dateCreated = datetime.datetime.strptime(session[0][1], "%Y-%m-%d %H:%M:%S")
    timePlayed = int((date - dateCreated).total_seconds())
    endSession = '''UPDATE Session SET date = ?, time_played = ? where id = ?'''
    cur.execute(endSession, (date, timePlayed, session[0][0]))
    mydb.commit()
    mydb.close()

    return redirect('/')