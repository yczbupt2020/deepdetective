import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
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
                'num_pages':paginator.num_pages,
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
