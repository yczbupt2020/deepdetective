import json
import urllib

from django.core import serializers
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from deepdetective.deepdetective_utils.login_util import loginValidator
from .. import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.views.decorators.csrf import csrf_exempt
import datetime
import time
import re
import requests
from bs4 import BeautifulSoup as bs


@csrf_exempt
def get_news(request):
    if request.method == "POST":
        news_list = models.News.objects.all().order_by("-date")
        # 将数据按照规定每页显示 10 条, 进行分割
        paginator = Paginator(news_list, 10)
        page = request.POST.get('page')
        try:
            news = paginator.page(page)
            news_json = serializers.serialize('json', news)
            error = None
            return HttpResponse(json.dumps({
                'page_content': news_json,
                'num_pages': paginator.num_pages,
                'error': error
            }))
        except PageNotAnInteger:
            # 如果请求的页数不是整数，返回错误信息
            error = "页面信息错误！"
            return HttpResponse(json.dumps({
                'page_content': None,
                'error': error
            }))
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回错误信息。
            error = "页面信息错误！"
            return HttpResponse(json.dumps({
                'page_content': None,
                'error': error
            }))

    else:
        error = "系统错误！"
        return HttpResponse(json.dumps({
            'page_content': None,
            'error': error
        }))


@csrf_exempt
def search_text(request):
    if request.method == "POST":
        query_text = request.POST.get('text')

        # 多个字段模糊查询， 括号中的下划线是双下划线，双下划线前是字段名，双下划线后可以是icontains或contains,区别是是否大小写敏感，竖线是或的意思
        # search_news = models.News.objects.filter(Q(title__icontains=query_text) \
        #                                          | Q(text__icontains=query_text))
        search_news = models.News.objects.filter(title__icontains=query_text)

        news_json = serializers.serialize('json', search_news)

        error = None
        return HttpResponse(json.dumps({
            'query_result': news_json,
            'error': error
        }))

    else:
        error = "系统错误！"
        return HttpResponse(json.dumps({
            'query_result': None,
            'error': error
        }))


def get_detail(request):
    validate = loginValidator(request)
    if validate != None:
        return validate
    if request.method == "GET":
        # 查询某个新闻
        query_id = request.GET.get('nid')
        search_news = models.News.objects.get(id=query_id)
        return render(request, 'user/detail.html', {'new': model_to_dict(search_news)})


# @csrf_exempt
# def get_detail(request):
#     if request.method == "POST":
#         #查询某个新闻
#         query_id = request.POST.get('news_id')
#
#         search_news = models.News.objects.get(id=query_id)
#
#         # news_json = serializers.serialize('json', search_news)
#
#         error = None
#         return render(request, 'user/detail.html',{'news':model_to_dict(search_news)})

# else:
#     error = "系统错误！"
#     return HttpResponse(json.dumps({
#         'query_result': None,
#         'error': error
#     }))

@csrf_exempt
def get_questiontext(request):
    if request.method == "POST":
        # 查询某个新闻
        query_id = request.POST.get('newsid')

        questiontext = models.Questiontext.objects.get(newsid=query_id)

        error = None
        return HttpResponse(json.dumps({'query_result': model_to_dict(questiontext)}))
    else:
        error = "系统错误！"
        return HttpResponse(json.dumps({
            'query_result': None,
            'error': error
        }))


@csrf_exempt
def get_checknews(request):
    if request.method == "POST":
        page = int(request.POST.get('page'))
        checknews_list = list(models.CheckNews.objects.all()[(page-1)*10:page*10].values())
        num = models.CheckNews.objects.all().count()
        return HttpResponse(json.dumps({
                'page_content': checknews_list,
                'num_pages': int(num/10+1),
                'error': None
            }))
        # checknews_list = models.CheckNews.objects.all().order_by('id')
        # print(checknews_list.values())
        # # 将数据按照规定每页显示 10 条, 进行分割
        # paginator = Paginator(checknews_list, 10)
        # page = int(request.POST.get('page'))
        # try:
        #     news = paginator.page(page)
        #     news_json = json.loads(json.dumps(news))
        #     error = None
        #     return HttpResponse(json.dumps({
        #         'page_content': news_json,
        #         'num_pages': paginator.num_pages,
        #         'error': error
        #     }))
        # except PageNotAnInteger:
        #     # 如果请求的页数不是整数，返回错误信息
        #     error = "页面信息错误！"
        #     return HttpResponse(json.dumps({
        #         'page_content': None,
        #         'error': error
        #     }))
        # except EmptyPage:
        #     # 如果请求的页数不在合法的页数范围内，返回错误信息。
        #     error = "页面信息错误！"
        #     return HttpResponse(json.dumps({
        #         'page_content': None,
        #         'error': error
        #     }))

    else:
        error = "系统错误！"
        return HttpResponse(json.dumps({
            'page_content': None,
            'error': error
        }))


@csrf_exempt
def get_linknews(request):
    validate = loginValidator(request)
    if validate != None:
        return validate
    if request.method == "GET":
        # 查询相似新闻
        query_id = request.GET.get('nid')
        link_news = list(models.LinkNews.objects.filter(checknewsid=query_id).values())
        return render(request, 'user/linkNews.html', {'linknews': link_news})


@csrf_exempt
def check_new(request):
    if request.method == "POST":
        # 查证
        title = request.POST.get('title')
        text = request.POST.get('text')
        firstdate = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        latestdate = firstdate
        newsmark = "0"
        newsid = None
        linkmark = "0"
        checkfakemark = "疑"
        # if title == None:
        #     title =''
        # if text == None:
        #     text =''
        # try:
        #     cur_checknew = models.CheckNews.objects.filter(Q(title=title)|Q(text=text))
        #     info = '该标题或内容曾被查证'
        # except models.CheckNews.DoesNotExist:
        #     try:
        #         new = models.News.objects.filter(Q(title=title)|Q(text=text))
        #         newsmark = 1
        #         newsid = new.pk
        #         checkfakemark = new.fakemark
        #         info='该标题或内容已被收录在库，请查看库内结果'
        #     except models.News.DoesNotExist:
        #         html = request.post(url='https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=' + title + text)
        #         print(html)
        #         result_list = re.findall("<div class=\"result c-container new-pmd\".*>(.*)</a>", html)
        #         if len(result_list) != 0:
        #             linkmark = 1
        #         info='该标题或内容建立查证成功，请查看结果'
        #     cur_checknew = models.CheckNews(
        #         title=title, text=text, firstdate=firstdate, latestdate=latestdate, newsmark=newsmark, newsid=newsid,
        #         linkmark=linkmark, checkfakemark=checkfakemark)
        #     cur_checknew.save()
        #     checknewsid = cur_checknew.pk
        #     if len(result_list) > 3:
        #         for i in range(0, 3):
        #             print(result_list[i])
        #     else:
        #         for i in range(0, len(result_list)):
        #             print(result_list[i])
        # return HttpResponse(json.dumps({
        #     'cur_checknew': cur_checknew,
        #     'info': info
        # }))
        status = 0  # 0：曾查证过；1：有对应库内数据（newsmark=1）；2：无库内数据（newsmark=0），有相似新闻；3：无库内数据，无相似新闻
        result_list = []
        if title == "":
            cur_checknew = list(models.CheckNews.objects.filter(text=text).values())
            if len(cur_checknew) != 0:
                print(cur_checknew)
                info = '该内容曾被查证'
            else:
                try:
                    new = models.News.objects.get(text=text)
                    newsmark = "1"
                    newsid = new.pk
                    checkfakemark = new.fakemark
                    info = '该内容有对应的库内数据，请查看'
                    status = 1
                except models.News.DoesNotExist:
                    result_list = get_checknew_result_list(text)
                    if len(result_list) != 0:
                        linkmark = "1"
                        status = 2
                    else:
                        status = 3
                    info = '该内容建立查证成功，请查看查证结果'
                cur_checknew = models.CheckNews(
                    title='空', text=text, firstdate=firstdate, latestdate=latestdate, newsmark=newsmark, newsid=newsid,
                    linkmark=linkmark, checkfakemark=checkfakemark)
                cur_checknew.save()
                checknewsid = cur_checknew.pk
                insert_linknews(checknewsid, result_list)
                cur_checknew = list(models.CheckNews.objects.filter(id=checknewsid).values())
        elif text == "":
            cur_checknew = list(models.CheckNews.objects.filter(title=title).values())
            if len(cur_checknew) != 0:
                print(cur_checknew)
                info = '该标题曾被查证'
            else:
                try:
                    new = models.News.objects.get(title=title)
                    newsmark = "1"
                    newsid = new.pk
                    checkfakemark = new.fakemark
                    info = '该标题有对应的库内数据，请查看'
                    status = 1
                except models.News.DoesNotExist:
                    result_list = get_checknew_result_list(title)
                    if len(result_list) != 0:
                        linkmark = "1"
                        status = 2
                    else:
                        status = 3
                    info = '该标题建立查证成功，请查看查证结果'
                cur_checknew = models.CheckNews(title=title, text='空', firstdate=firstdate, latestdate=latestdate,
                                                newsmark=newsmark, newsid=newsid, linkmark=linkmark,
                                                checkfakemark=checkfakemark)
                cur_checknew.save()
                checknewsid = cur_checknew.pk
                # checknewsid = 1
                insert_linknews(checknewsid, result_list)
                cur_checknew = list(models.CheckNews.objects.filter(id=checknewsid).values())
        else:
            cur_checknew = list(models.CheckNews.objects.filter(Q(title=title) | Q(text=text)).values())
            if len(cur_checknew) != 0:
                print(cur_checknew)
                info = '该标题或内容曾被查证'
            else:
                try:
                    new = models.News.objects.filter(Q(title=title) | Q(text=text))[0]
                    newsmark = "1"
                    newsid = new.pk
                    checkfakemark = new.fakemark
                    info = '该标题及内容有对应的库内数据，请查看'
                    status = 1
                except models.News.DoesNotExist:
                    result_list = get_checknew_result_list(title + ' ' + text)
                    if len(result_list) != 0:
                        linkmark = "1"
                        status = 2
                    else:
                        status = 3
                    info = '该标题及内容建立查证成功，请查看查证结果'
                cur_checknew = models.CheckNews(
                    title=title, text=text, firstdate=firstdate, latestdate=latestdate, newsmark=newsmark,
                    newsid=newsid,linkmark=linkmark, checkfakemark=checkfakemark)
                cur_checknew.save()
                checknewsid = cur_checknew.pk
                insert_linknews(checknewsid, result_list)
                cur_checknew = list(models.CheckNews.objects.filter(id=checknewsid).values())
        return HttpResponse(json.dumps({
            'cur_checknew': cur_checknew,
            'info': info,
            'status': status
        }))
    else:
        error = "系统错误！"
        return HttpResponse(json.dumps({
            'cur_checknew': None,
            'info': error,
            'status': 'SYSERROR'
        }))


@csrf_exempt
def refresh_checknew(request):
    if request.method == "POST":
        checknew_id = request.POST.get('checknew_id')
        cur_checknew = models.CheckNews.objects.get(id=checknew_id)
        if cur_checknew.newsmark == "0":
            try:
                new = models.News.objects.get(Q(title=cur_checknew.title) & Q(text=cur_checknew.text))
                cur_checknew.newsmark = "1"
                cur_checknew.newsid = new.pk
                cur_checknew.checkfakemark = new.fakemark
                cur_checknew.latestdate = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                cur_checknew.save()
                info = '数据已改变，发现对应入库数据'
            except models.News.DoesNotExist:
                result_list = get_checknew_result_list(cur_checknew.title + ' ' + cur_checknew.text)
                if len(result_list) != 0:
                    models.LinkNews.objects.filter(checknewsid=checknew_id).delete()
                    cur_checknew.linkmark = "1"
                    # checkfakemark怎么更新？
                    cur_checknew.latestdate = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    cur_checknew.save()
                    insert_linknews(checknew_id, result_list)
                    info = '数据已改变，更新相似新闻'
                    # 把相似新闻插入表中

                else:
                    info = '数据未改变，无相似新闻'
        else:
            info = '数据未改变，已存在对应入库数据'
        cur_checknew = list(models.CheckNews.objects.filter(id=checknew_id).values())
        print(cur_checknew)
        return HttpResponse(json.dumps({
            'cur_checknew': cur_checknew,
            'info': info
        }))
    else:
        error = "系统错误！"
        return HttpResponse(json.dumps({
            'page_content': None,
            'info': error
        }))


def insert_linknews(checknewsid, result_list):
    listlen = len(result_list)
    if listlen > 3:
        listlen = 3
    for i in range(0, listlen):
        result = result_list[i]
        print('\n')
        # print(result)
        web = result.a['href']
        title = result.a.get_text()
        print(title)
        try:
            datestr = result.find(name='span',attrs={'class': 'newTimeFactor_before_abs c-color-gray2 m'}).get_text()
        except:
            datestr = result.find(name='span', attrs={'class': ' newTimeFactor_before_abs c-color-gray2 m'})
        print(datestr)
        date=datestr.replace('\xa0','').replace(' ','')
        if '天前' in date:
            num = int(date.repalce('天前', ''))
            date = str((datetime.datetime.now() - datetime.timedelta(days=num)).strftime("%Y-%m-%d"))

        tmp = time.strptime(date, u"%Y年%m月%d日")
        new_date = time.strftime("%Y-%m-%d", tmp)
        text = result.find(name='div', attrs={'class': 'c-abstract'}).get_text().replace(datestr, '')
        source = result.find(name='a', attrs={'class': 'c-showurl c-color-gray'}).get_text()
        linknew = models.LinkNews(checknewsid=checknewsid, title=title, text=text, date=new_date,
                                  comparesource=source, compareweb=web)
        linknew.save()


def get_checknew_result_list(content):
    url = 'http://www.baidu.com.cn/s?wd=' + urllib.parse.quote(content) + '&pn=0'
    r = requests.get(url=url)
    soup = bs(r.content, "html.parser")
    result_list = soup.find_all(name='div', attrs={'class': 'result c-container new-pmd'})
    return result_list
