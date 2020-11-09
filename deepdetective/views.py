from django.shortcuts import render

from deepdetective.deepdetective_utils.login_util import loginValidator
# Create your views here.

#页面跳转
def main_user(request):
    validate = loginValidator(request)
    if validate != None:
        return validate
    return render(request, 'user/userMain.html', {'username':request.session.get('username')})

def check_user(request):
    validate = loginValidator(request)
    if validate != None:
        return validate
    return render(request, 'user/userCheck.html', {'username': request.session.get('username')})