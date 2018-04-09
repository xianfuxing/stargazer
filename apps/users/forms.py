import re
from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import get_user_model
User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, error_messages={'required': '请输入用户名'})
    password = forms.CharField(required=True, min_length=5, error_messages={'required': '请输入密码'})


class CaptchaLoginForm(LoginForm):
    captcha = CaptchaField(required=True, error_messages={'required': '请输入验证码'})


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '用户'
        self.fields['email'].label = '邮件'
        self.fields['department'].label = '部门'
        self.fields['position'].label = '职位'
        self.fields['phone'].label = '电话'

    class Meta:
        model = User
        fields = ['username', 'email', 'department', 'position', 'phone']

    def clean_phone(self):
        mobile = self.cleaned_data.get('phone', '')
        regex_mobile = '^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$'
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号不符合', code='invalid_mobile')
