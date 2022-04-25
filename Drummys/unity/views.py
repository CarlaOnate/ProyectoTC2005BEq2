from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import loads, dumps
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
def login(req):
    body_unicode = req.body.decode('utf-8')
    body = loads(body_unicode)

    username = body["username"]
    password = body["password"]
    print('\n\n', username, password, '\n\n')

    mydb = sqlite3.connect("DrummyDB.db")
    cur = mydb.cursor()

    # Find user with that username and password
    findUserSql = '''SELECT User.id, User.username, User.age, Countries.name, Countries.id, Countries.nickname 
    FROM User INNER JOIN Countries ON Countries.id=User.country_id WHERE User.username=? AND User.password=?'''
    # (id, username, password, age, countryName, countryId, countryNickname)
    user = cur.execute(findUserSql, (username, password,)).fetchall()
    # todo revisar que se regresa a unity

    if not user:
        return JsonResponse({"error": "User not found"})
    else:
        # If user exists create session and return session id
        userId = user[0][0]
        userUsername = user[0][1]
        userAge = user[0][2]
        userCountryName = user[0][3]
        userCountryId = user[0][4]
        userCountryNickname = user[0][5]

        dateCreated = datetime.datetime.now().replace(microsecond=0)
        print('\n\nDateCreated =>', dateCreated, '\n\n')
        createSessionSql = '''INSERT INTO Session (user_id, dateCreated) VALUES (?, ?)'''
        cur.execute(createSessionSql, (userId, dateCreated))
        retrieveSessionSql = '''SELECT id FROM Session WHERE user_id=? AND dateCreated=?;'''
        session = cur.execute(retrieveSessionSql, (str(userId), dateCreated)).fetchall()
        mydb.commit()
        json = dumps({
            "user_id": userId,
            "username": userUsername,
            "age": userAge,
            "countryId": userCountryId,
            "countryName": userCountryName,
            "countryNickname": userCountryNickname,
            "session_id": session[0][0]
        })
        mydb.close()
        return HttpResponse(json, content_type="text/json-comment-filtered")
