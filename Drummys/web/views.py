from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, Countries, Session, Download
from json import loads,dumps
from django.contrib.auth import authenticate, login as loginUser, logout
from .models import CustomUser, Countries, Session
from django.contrib.auth.decorators import login_required
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
    cur.execute(stringSQL, (ip, device, dateCreated,))
    mydb.commit()
    mydb.close()
    return render(request, 'web/index.html')

#  --- GRAPHS ---
def topscores_global(request):
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''SELECT Party.id, User.id as User_ID, User.username, Countries.nickname as Country, 
    Party.total_score, Party.dateCreated FROM  Party
    INNER JOIN User, Countries ON Party.user_id = User.id  AND Countries.id = User.country_id 
    ORDER BY Party.total_score LIMIT 10 '''
    rows = cur.execute(stringSQL)
    if rows is None:
        raise Http404("user_id does not exist")
    else:
        lista_salida = [["Username", "Country", "Total Score (s)", "Date"]]
        for r in rows:
            date = datetime.datetime.strptime(r[5], "%Y-%m-%d %H:%M:%S").strftime("%A %d. %b")
            d = [r[2], r[3], r[4], date]
            lista_salida.append(d)
        j = dumps(lista_salida)
    mydb.close()
    return j

def graficaGlobalLevel(level):
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''SELECT Levels.id as Lvl_ID, User.id as User_ID,User.username, Countries.name as Country, 
Party.id as Party_id, Levels.difficulty as level,  Levels.final_time, Levels.penalties, 
Levels.dateCreated 
FROM  Levels INNER JOIN User, Countries, Party ON Levels.user_id = User.id  AND Party.id=Levels.party_id AND 
Countries.id = User.country_id WHERE Levels.difficulty= ? ORDER BY Levels.final_time  
LIMIT 10'''
    rows = cur.execute(stringSQL, (level,))
    if rows is None:
        raise Http404("user_id or level does not exist")
    else:
        lista_salida = []
        for r in rows:
            fixed_date = datetime.datetime.strptime(r[8], "%Y-%m-%d %H:%M:%S").strftime("%A %d. %b %Y")
            html_tooltip = '''<div style="margin: 10px; text-align: left; font-size: 14px; color: black;">''' + "<b>" + str(fixed_date) + "</b><br>" + '''<p style="color: #858585; font-size: 14px;">Score:</p>''' + '''<p style="color: #4285f4; font-weight: bold; font-size: 16px;">''' + str(r[6]) + "</p>" + "</div>"
            d = [r[2], r[6], html_tooltip, 'color: #4285f4']
            lista_salida.append(d)
        j = dumps(lista_salida)

    title = 'Top 10 fastest users in level ' + str(level)
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
    Party.id as Party_id, Levels.difficulty as level,  Levels.final_time, Levels.penalties, Levels.dateCreated 
    FROM  Levels INNER JOIN User, Countries, Party ON Levels.user_id = User.id  AND Party.id=Levels.party_id AND 
    Countries.id = User.country_id WHERE Levels.user_id = ?  AND Levels.difficulty= ? ORDER BY Levels.final_time  
    LIMIT 10'''
    rows = cur.execute(stringSQL, (usuario, level, ))
    if rows is None:
        raise Http404("user_id does not exist")
    else:
        lista_salida = [['Date', 'Time (s)']]
        for r in rows:
            date = datetime.datetime.strptime(r[8], "%Y-%m-%d %H:%M:%S").strftime("%A %d. %b")
            d = [date, r[6]]
            lista_salida.append(d)
        j = dumps(lista_salida)
    title = 'Your top 10 scores in level  ' + str(level)
    modified_title = dumps(title)
    mydb.close()
    return({
        'values': j,
        'title': modified_title
    })

def user_sessions(usuario):
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''SELECT SUM(time_played) AS total, date FROM Session WHERE Session.user_id = ? AND Session.date
    Group by date Order by time_played asc'''
    rows = cur.execute(stringSQL, (usuario,))
    if rows is None:
        raise Http404("user_id does not exist")
    else:
        lista_salida = [['Date', 'Time (s)']]
        for r in rows:
            if r[0] is not None and r[1] is not None:
                date = datetime.datetime.strptime(r[1], "%Y-%m-%d %H:%M:%S").strftime("%A %d. %b")
                d = [date, r[0]]
                lista_salida.append(d)
        j = dumps(lista_salida)
    mydb.close()
    return j

def user_topscores(usuario):
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''SELECT Party.id, User.id as User_ID, User.username, Countries.name as Country, 
Party.total_score, Party.dateCreated FROM  Party
 INNER JOIN User, Countries ON Party.user_id = User.id  AND Countries.id = User.country_id WHERE Party.user_id = ? 
 ORDER BY Party.total_score LIMIT 10 '''
    rows = cur.execute(stringSQL, (str(usuario),))
    if rows is None:
        raise Http404("user_id does not exist")
    else:
        lista_salida = [["Username", "Country", "Total Score (s)", "Date"]]
        for r in rows:
            print('\n\n date =>', r[5])
            date = datetime.datetime.strptime(r[5], "%Y-%m-%d %H:%M:%S").strftime("%A %d. %b")
            d = [r[2], r[3], r[4], date]
            lista_salida.append(d)
        j = dumps(lista_salida)
    mydb.close()
    return j

def user_visits(req):
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    stringSQL = '''select COUNT (*), dateCreated from Visit where 
    DATE(dateCreated, 'start of day') = DATE(Visit.dateCreated, 'start of day') 
    group by DATE(dateCreated, 'start of day') LIMIT 10;'''
    rows = cur.execute(stringSQL)
    if not rows:
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

@login_required
def myStats(req):
    user = CustomUser.objects.get(username=req.user)
    id = user.id
    topscores = user_topscores(id) # seria pasar el req.user
    sessions = user_sessions(id) # seria pasar el req.user
    level1 = user_level(1, id) # seria pasar el req.user
    level2 = user_level(2, id) # seria pasar el req.user
    level3 = user_level(3, id) # seria pasar el req.user
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

@login_required
def dashboard(request):
    id = request.user.id
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    getUserSql = '''SELECT User.id, User.username, Countries.name as Country, User.age FROM User
        , Countries WHERE User.id = ? AND Countries.id = User.country_id;'''
    user = cur.execute(getUserSql, (id,)).fetchall()
    mydb.commit()
    mydb.close()

    return render(request, 'web/dashboard.html', {"id": user[0][0], "username": user[0][1], "country": user[0][2], "age": user[0][3]})

def download(request):
    return render(request, 'web/download.html')

@login_required
def download_logged(request):
    return render(request, 'web/download-logged.html')

def thankyou(request):
    return render(request, 'web/thankyou.html')

def login(request):
    return render(request, 'web/login.html')

def profile(request):
    return render(request, 'web/profile.html')

def signup(req):
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    allUsernames = list(CustomUser.objects.all().values_list('username', flat=True))

    print('\n\n allUsernames =>', allUsernames, '\n\n')

    findUserSql = '''SELECT * From Countries'''
    countries = cur.execute(findUserSql).fetchall()
    countriesArr = []
    for el in countries:
        countriesArr.append(el[2])
    countriesJson = dumps(countriesArr)
    mydb.close()
    return render(req, 'web/signup.html', {"countries": countriesJson, "usernames": allUsernames})

# ------ AUTH ---------
def authLogin(req):
    username = req.POST["username"]
    password = req.POST["password"]
    print('\n\n', username, password, '\n\n')

    authenticatedUsername = authenticate(req, username=username, password=password)

    if authenticatedUsername is not None:
        user = CustomUser.objects.get(username=authenticatedUsername)
        loginUser(req, authenticatedUsername)
        print('\n\n req.user after login =>', req.user, '\n\n')
        dateCreated = datetime.datetime.now().replace(microsecond=0)
        print('\n\n dateCreated =>', dateCreated, '\n\n')
        session = Session.objects.create(user_id=user.id, datecreated=dateCreated)
        return redirect('dashboard')
    else:
        return render(req, 'web/login.html', {"error": "Datos incorrectos"})

@csrf_exempt
def authSignup(req):
    username = req.POST["username"]
    age = req.POST["age"]
    password = req.POST["password"]
    country = req.POST["country"]

    countryInstance = Countries.objects.get(name=country)
    user = CustomUser.objects.create_user(username=username, country=countryInstance, password=password, age=age)
    user.save()
    return redirect('thankyou')

@login_required
@csrf_exempt
def updateUser(req):
    id = req.user.id
    username = req.POST["username"]

    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    updateUserSql = '''UPDATE User SET username = ? WHERE id=?;'''
    cur.execute(updateUserSql, (username, id,))
    mydb.commit()
    mydb.close()

    return JsonResponse({"msg": 200})


@login_required
def getUser(req):
    id = req.user.id
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    getUserSql = '''SELECT User.id, User.username, Countries.name as Country, User.age FROM User
    , Countries WHERE User.id = ? AND Countries.id = User.country_id;'''
    user = cur.execute(getUserSql, (id,)).fetchall()
    mydb.commit()
    mydb.close()

    return JsonResponse({"id": user[0][0], "username": user[0][1], "country": user[0][2], "age": user[0][3]})

@login_required
def authLogout(req):
    id = req.user.id
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()

    retrieveSessionSql = '''SELECT id, dateCreated FROM Session WHERE user_id=? AND date IS NULL AND time_played IS NULL;'''
    session = cur.execute(retrieveSessionSql, (id,)).fetchall()

    date = datetime.datetime.now().replace(microsecond=0)
    dateCreated = datetime.datetime.strptime(session[0][1], "%Y-%m-%d %H:%M:%S")
    timePlayed = int((date - dateCreated).total_seconds())
    endSession = '''UPDATE Session SET date = ?, time_played = ? where id = ?'''
    cur.execute(endSession, (date, timePlayed, session[0][0],))
    mydb.commit()
    mydb.close()

    logout(req)

    return redirect('/')

# --- API ---
@login_required
def addDownload(req):
    device = req.META.get('HTTP_USER_AGENT')
    user = CustomUser.objects.get(username=req.user)
    dateCreated = datetime.datetime.now().replace(microsecond=0)
    Download.objects.create(user_id= user.id, device=device, datecreated=dateCreated)
    return JsonResponse({"msg": 200})