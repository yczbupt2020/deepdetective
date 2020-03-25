from django.db import models


# Create your models here.

class Login(models.Model):
    roleTuple = (
        (0, "user"),
    )
    username = models.CharField(max_length=15, primary_key=True, unique=True)
    password = models.CharField(max_length=45, default=None)
    role = models.IntegerField(choices=roleTuple)


# 用户实体
class User(models.Model):
    genderTuple = (
        (0, "unknown"),
        (1, "male"),
        (2, "female"),
    )
    userid = models.CharField(max_length=15, primary_key=True)
    username = models.CharField(max_length=45)
    gender = models.IntegerField(choices=genderTuple)
