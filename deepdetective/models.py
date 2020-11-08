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

# # 谣言（较真平台爬取，已有标签）
# class News(models.Model):
#     title = models.CharField(max_length=200)
#     text = models.TextField()
#     date = models.DateTimeField(blank=True, null=True)
#     quickshow = models.CharField(max_length=100, blank=True, null=True)
#     fakemark = models.CharField(max_length=5)
#     fakemarktext = models.CharField(max_length=20)
#     checkcontenttext = models.TextField()
#     checkcontentwriter = models.CharField(max_length=45)
#     checkcontecttype = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'news'
#
# # 每个谣言对应的描述，详情页
# class Questiontext(models.Model):
#     newsid = models.ForeignKey(News, models.DO_NOTHING, db_column='newsid')
#     htmlcontext = models.TextField()
#
#     class Meta:
#         managed = False
#         db_table = 'questiontext'

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

    # class Meta:
    #     managed = False
    #     db_table = 'news'

# 每个谣言对应的描述，详情页
class Questiontext(models.Model):
    newsid = models.ForeignKey(News, models.DO_NOTHING, db_column='newsid')
    htmlcontext = models.TextField()

    # class Meta:
    #     managed = False
    #     db_table = 'questiontext'

# 谣言查证，前端输入的新闻
class CheckNews(models.Model):
    title = models.CharField(max_length=200)  #输入标题，标题与内容缺一不可
    text = models.TextField() #输入内容
    # newsdate = models.DateTimeField()
    firstdate = models.DateTimeField() #创建查证时间
    latestdate = models.DateTimeField() #创建查证时间 #更新时间
    # img = models.ImageField(upload_to='img') #上传的图片
    newsmark = models.CharField(max_length=5) #是否入库（新闻是否已在news表中），课通过fakemark盘算是否已查证
    # newsid = models.ForeignKey(News, models.DO_NOTHING, db_column='newsid') #已入库的新闻ID，news表外键
    newsid = models.IntegerField(max_length=20) #已入库的新闻ID，可能为空，所以不能用外键
    linkmark = models.CharField(max_length=5) #是否有类似的新闻
    checkfakemark = models.CharField(max_length=5) #自定义算法对新闻的辨别结果,newsmark=1则该值为news_fakemark


    class Meta:
        managed = False
        db_table = 'deepdetective_checknews'

#类似的新闻
class LinkNews(models.Model):
    # checknewsid = models.ForeignKey(CheckNews, models.DO_NOTHING, db_column='checknewsid')  # 待查证的新闻
    checknewsid = models.IntegerField(max_length=20)
    title = models.CharField(max_length=200, blank=True, null=True) #标题
    text = models.TextField(blank=True, null=True) #内容
    date = models.DateTimeField(blank=True, null=True) #发布时间
    comparesource = models.CharField(max_length=45, blank=True, null=True) #新闻源
    compareweb = models.CharField(max_length=100, blank=True, null=True) #网页链接

    class Meta:
        managed = False
        db_table = 'deepdetective_linknews'