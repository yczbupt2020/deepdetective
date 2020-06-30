from django.shortcuts import redirect
from django.shortcuts import render
from .. import models
from .. import forms
from .captcha_util import captcha
from .captcha_util import jarge_captcha
from ..models import User


# ***********************登录登出相关***********************
# 登录验证器，验证是否登录
def loginValidator(request):
    print(request.session.get('is_login', None))
    print(request.session.get('userid'))
    if not request.session.get('is_login', None) and (request.session.get('userid') == None):
        return redirect('/login/')
    else:
        # 登录了转发到对应主页面
        role = request.session.get('role')
        if role == 0:
            if 'user' not in request.get_full_path_info():
                return redirect('/user/')
            else:
                return None


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        # 登录了转发到对应主页面
        role = request.session.get('role')
        if role == 0:
            return redirect('/user/')
    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        error = "<h6>登录错误！</h6><span>请检查输入</span>"
        # 先验证验证码是否正确
        capt = request.POST.get('captcha', None)  # 用户提交的验证码
        key = request.POST.get('hashkey', None)  # 验证码答案
        if not jarge_captcha(capt, key):
            error = "<h6>登录错误！</h6><span>验证码错误</span>"
            return render(request, 'login.html', locals())
        else:
            cap = captcha()
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                login_user = models.Login.objects.get(username=username)
            except:
                error = "<h6>登录错误！</h6><span>用户名不存在</span>"
                return render(request, 'login.html', locals())
            if login_user.password == password:
                request.session['role'] = login_user.role
                if login_user.role == 0:  # 用户
                    user = models.User.objects.get(userid=username)
                    request.session['is_login'] = True
                    request.session['userid'] = username
                    request.session['username'] = user.username
                    request.session['role'] = login_user.role
                    return redirect('/user/')
            else:
                error = "<h6>登录错误！</h6><span>密码错误</span>"
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())
    else:
        login_form = forms.LoginForm()
        registration_form = forms.RegistrationForm()
        cap = captcha()
        return render(request, 'login.html', locals())


# 注册
def registration(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        # 登录了转发到对应主页面
        role = request.session.get('role')
        if role == 0:
            return redirect('/user/')
    if request.method == "POST":
        registration_form = forms.RegistrationForm(request.POST)
        error = "<h6>注册失败！</h6><span>请检查输入</span>"
        if registration_form.is_valid():
            userid = registration_form.cleaned_data.get('userid')
            password = registration_form.cleaned_data.get('password')
            username = registration_form.cleaned_data.get('username')
            gender = registration_form.cleaned_data.get('gender')
            if gender == '':
                gender = 0
            models.Login.objects.create(username=userid, password=password, role=0)
            models.User.objects.create(userid=userid, username=username, gender=int(gender))
            request.session['is_login'] = True
            request.session['userid'] = userid
            request.session['username'] = username
            request.session['role'] = 0
            return redirect('/user/')
        else:
            error = "<h6>注册失败！</h6><span>请检查输入</span>"
            return render(request, 'login.html', locals())
    else:
        login_form = forms.LoginForm()
        registration_form = forms.RegistrationForm()
        cap = captcha()
        return render(request, 'login.html', locals())


# 登出
def logout(request):
    loginValidator(request)
    request.session.flush()
    return redirect("/login/")
