from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    username = models.TextField(unique=True)
    country_id = models.IntegerField()
    password = models.TextField()
    age = models.IntegerField()