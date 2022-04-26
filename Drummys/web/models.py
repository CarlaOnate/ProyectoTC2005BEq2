from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class Countries(models.Model):
    nickname = models.TextField(db_column='Nickname', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        db_table = 'Countries'

class CustomUser(AbstractUser):
    pass
    username = models.TextField(unique=True, blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Countries, on_delete=models.RESTRICT, null=True, blank=True)
    age = models.IntegerField(blank=True, null=True)
    is_authenticated = True
    is_anonymous = False
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['age']
    class Meta:
        db_table = 'User'


class Download(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    device = models.TextField(blank=True, null=True)
    datecreated = models.TextField(db_column='dateCreated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Download'


class Levels(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    party_id = models.IntegerField(blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)
    final_time = models.IntegerField(blank=True, null=True)
    penalties = models.IntegerField(blank=True, null=True)
    datecreated = models.TextField(db_column='dateCreated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Levels'


class Party(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    session_id = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    datecreated = models.TextField(db_column='dateCreated', blank=True, null=True)  # Field name made lowercase.
    penalties = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Party'


class Session(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    time_played = models.IntegerField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    datecreated = models.TextField(db_column='dateCreated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Session'


class Visit(models.Model):
    ip = models.TextField(blank=True, null=True)
    device = models.TextField(blank=True, null=True)
    datecreated = models.TextField(db_column='dateCreated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Visit'