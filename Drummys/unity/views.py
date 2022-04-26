from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import loads,dumps
from web.models import CustomUser, Countries, Session
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
        raise Http404("It was not possible to register party data")
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

    return JsonResponse({"party_id": partyId})

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

    return JsonResponse({"party_id": partyId})


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
            "user": {
                "id": user.id,
                "username": user.username,
                "age": user.age,
                "countryId": userCountry.id,
                "countryName": userCountry.name,
                "countryNickname": userCountry.nickname,
            },
            "session": {
                "id": session.id
            }
        })
        return JsonResponse(json, safe=False)
    else:
        return JsonResponse({"error": "Algo salió mal, upsi"})


@login_required
def authLogout(req):
    id = req.user.id  # todo: se sacaría de req.user
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

    logout(req)

    return HttpResponse(dumps({"msg": "Goodbye!"}))
