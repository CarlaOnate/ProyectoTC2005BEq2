from django.db import models

class Countries(models.Model):
    # Campos
    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)

class User(models.Model):
    # Campos
    username = models.CharField(max_length=20)
    age = models.IntegerField()
    password = models.CharField(max_length=20)
    country_id = models.ForeignKey(Countries, on_delete=models.PROTECT)



