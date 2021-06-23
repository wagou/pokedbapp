from django.db import models
from mysite.settings import BASE_DIR
from django.utils import timezone

# Create your models here.

class KP(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20,null=True)
    count = models.IntegerField()
    count2 = models.IntegerField(default=0)

    class Meta:
        db_table = 'KP'

class User(models.Model):
    twid = models.CharField(max_length=30,null=True, unique=True)
    key = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'Users'

class Battledetail(models.Model):
    key = models.CharField(max_length=20,null=True)
    date = models.CharField(max_length=20,null=True)
    poke1 = models.CharField(max_length=20,null=True)
    poke2 = models.CharField(max_length=20,null=True)
    poke3 = models.CharField(max_length=20,null=True)
    poke4 = models.CharField(max_length=20,null=True)
    poke5 = models.CharField(max_length=20,null=True)
    poke6 = models.CharField(max_length=20,null=True)
    mypoke1 = models.CharField(max_length=20,null=True)
    mypoke2 = models.CharField(max_length=20,null=True)
    mypoke3 = models.CharField(max_length=20,null=True)
    mypoke4 = models.CharField(max_length=20,null=True)
    mypoke5 = models.CharField(max_length=20,null=True)
    mypoke6 = models.CharField(max_length=20,null=True)
    battletype = models.CharField(max_length=20,null=True)
    memory = models.CharField(max_length=5,null=True)

    class Meta:
        db_table = 'Battledetails'
