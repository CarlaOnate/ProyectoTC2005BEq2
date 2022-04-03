from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
import datetime
import sqlite3

# Create your views here.
def index(req):
    return HttpResponse('<p>Soy Index</p>')

@csrf_exempt
def signup(req):
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
    # Todo: Que pasa si algo sale mal? Regresar error
    return JsonResponse({"user": {"id": user[0][0]}})

@csrf_exempt
def login(req):
    username = req.POST["username"]
    password = req.POST["password"]

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
        return JsonResponse([{
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
        }], safe=False)