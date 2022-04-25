from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import loads,dumps
from web.models import CustomUser, Countries, Session
from django.contrib.auth import authenticate, login
from django.http import Http404
import datetime
import sqlite3
# Create your views here.

@csrf_exempt
def game_party(request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)

    party_id = body['party_id']
    total_score = body['total_score']
    time_played = body['time_played']
    penalties = body['penalties']

    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()

    stringSQL = '''UPDATE Party SET total_score = ?, time_played = ?, penalties = ? 
    WHERE Party.id = ?;'''

    rows = cur.execute(stringSQL, (total_score, time_played, penalties, party_id))
    mydb.commit()

    if rows is None:
        return JsonResponse({"error": "It was not possible to register party data"})
    else:
        d = {"msg": "200"}
        j = dumps(d)

    mydb.close()
    return HttpResponse(j, content_type="text/json-comment-filtered")

@csrf_exempt
def registerFirstLevel(req):
    userId = req.POST["user_id"]
    sessionId = req.POST["session_id"]
    difficulty = req.POST["difficulty"]
    playedAudio = req.POST["played_audio"]
    finalTime = req.POST["final_time"]
    penalties = req.POST["penalties"]

    #Since it's first level we need to create the party
    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    dateCreated = datetime.datetime.now().replace(microsecond=0)
    dateCreated.replace(microsecond=0)

    createPartySql = '''INSERT INTO Party (USER_ID, SESSION_ID, DATECREATED) VALUES (?, ?, ?)'''
    cur.execute(createPartySql, (userId, sessionId, dateCreated))

    findPartySql = '''SELECT id FROM Party WHERE user_id=? AND session_id=? order by dateCreated DESC'''
    partyId = cur.execute(findPartySql, (userId, sessionId)).fetchall()[0][0]

    createLevel1Sql = '''INSERT INTO Levels (USER_ID, PARTY_ID, DIFFICULTY, PLAYED_AUDIO, FINAL_TIME, PENALTIES, DATECREATED) VALUES (?, ?, ?, ?, ?, ?, ?)'''
    cur.execute(createLevel1Sql, (userId, partyId, difficulty, playedAudio, finalTime, penalties, dateCreated))
    mydb.commit()
    mydb.close()

    return HttpResponse(dumps({"party_id": partyId}), content_type="text/json-comment-filtered")

@csrf_exempt
def registerLevel(req):
    userId = req.POST["user_id"]
    partyId = req.POST["party_id"]
    difficulty = req.POST["difficulty"]
    playedAudio = req.POST["played_audio"]
    finalTime = req.POST["final_time"]
    penalties = req.POST["penalties"]

    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()
    dateCreated = datetime.datetime.now().replace(microsecond=0)
    dateCreated.replace(microsecond=0)

    createLevelSql = '''INSERT INTO Levels (USER_ID, PARTY_ID, DIFFICULTY, PLAYED_AUDIO, FINAL_TIME, PENALTIES, DATECREATED) VALUES (?, ?, ?, ?, ?, ?, ?)'''
    cur.execute(createLevelSql, (userId, partyId, difficulty, playedAudio, finalTime, penalties, dateCreated))
    mydb.commit()
    mydb.close()

    return HttpResponse(dumps({"party_id": partyId}), content_type="text/json-comment-filtered")


@csrf_exempt
def level(req):
    difficulty = req.POST["difficulty"]
    if difficulty == "1":
        return registerFirstLevel(req)
    elif (difficulty == "2") | (difficulty == "3"):
        return registerLevel(req)
    else:
        return JsonResponse({"error": "Numero de dificultad no es valida"})

@csrf_exempt
def authLogin(req):
    username = req.POST["username"]
    password = req.POST["password"]
    authenticatedUsername = authenticate(req, username=username, password=password)
    if authenticatedUsername is not None:
        user = CustomUser.objects.get(username=authenticatedUsername)
        userCountry = Countries.objects.get(pk=user.country.id)
        login(req, authenticatedUsername)
        dateCreated = datetime.datetime.now().replace(microsecond=0)
        session = Session.objects.create(user_id=user.id, datecreated=dateCreated)
        json = dumps({
            "user_id": user.id,
            "username": user.username,
            "age": user.age,
            "countryId": userCountry.id,
            "countryName": userCountry.name,
            "countryNickname": userCountry.nickname,
            "session_id": session.id
        })
        mydb.close()
        return HttpResponse(json, content_type="text/json-comment-filtered")
