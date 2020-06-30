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

# 谣言（较真平台爬取，已有标签）
class News(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField(blank=True, null=True)
    quickshow = models.CharField(max_length=100, blank=True, null=True)
    fakemark = models.CharField(max_length=5)
    fakemarktext = models.CharField(max_length=20)
    checkcontenttext = models.TextField()
    checkcontentwriter = models.CharField(max_length=45)
    checkcontecttype = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'news'

# 每个谣言对应的描述，详情页
class Questiontext(models.Model):
    newsid = models.ForeignKey(News, models.DO_NOTHING, db_column='newsid')
    htmlcontext = models.TextField()

    class Meta:
        managed = False
        db_table = 'questiontext'
