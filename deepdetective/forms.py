from django import forms
from captcha.fields import *
from . import models


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "用户名", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "密码"}))


class RegistrationForm(forms.Form):
    userid = forms.CharField(label="用户名", max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "用户名", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "密码"}))
    username = forms.CharField(label="昵称", max_length=45,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "昵称"}))
    gender = forms.ChoiceField(label="性别",
                               choices=(('1', '男'), ('2', '女'),), initial='0', required=False,
                               widget=forms.RadioSelect())
