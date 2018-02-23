from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, error_messages={'required': '请输入用户名'})
    password = forms.CharField(required=True, min_length=5, error_messages={'required': '请输入密码'})