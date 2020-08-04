import json

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
