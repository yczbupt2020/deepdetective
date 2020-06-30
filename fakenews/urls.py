"""fakenews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from deepdetective.deepdetective_utils import captcha_util
from deepdetective.deepdetective_utils import login_util
from django.urls import include
from deepdetective import views
from deepdetective.controller import user_controller

urlpatterns = [
    path('admin/', admin.site.urls),
    # ***********登录、登出*************
    path('login/', login_util.login),
    path('registration/', login_util.registration),
    path('captcha/', include('captcha.urls')),
    path('refresh_captcha/', captcha_util.refresh_captcha),
    path('logout/', login_util.logout),

    path('user/', views.main_user),
    # 获取分页的谣言信息
    path('user/get_page_news/', user_controller.get_news),
]
