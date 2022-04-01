# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Countries(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    nickname = models.TextField()

    class Meta:
        managed = False
        db_table = 'Countries'


class Download(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    device = models.TextField(blank=True, null=True)
    datecreated = models.TextField(db_column='dateCreated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Download'


class Levels(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    party_id = models.IntegerField(blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)
    played_audio = models.IntegerField(blank=True, null=True)
    final_time = models.IntegerField(blank=True, null=True)
    penalties = models.IntegerField(blank=True, null=True)
    datecreated = models.TextField(db_column='dateCreated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Levels'


class Party(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    session_id = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    time_played = models.IntegerField(blank=True, null=True)
    datecreated = models.TextField(db_column='dateCreated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Party'


class Session(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    time_played = models.IntegerField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    datecreated = models.TextField(db_column='dateCreated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Session'


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.TextField(unique=True)
    country_id = models.IntegerField()
    password = models.TextField()
    age = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'User'


class Visit(models.Model):
    id = models.BigAutoField(primary_key=True)
    ip = models.TextField(blank=True, null=True)
    device = models.TextField(blank=True, null=True)
    datecreated = models.TextField(db_column='dateCreated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Visit'
