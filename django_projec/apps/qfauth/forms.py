
from django import forms
from apps.forms import FormMixin
from django.core import validators
from django.core.cache import cache
from apps.qfauth.models import User


class LoginForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11,min_length=11)
    password = forms.CharField(max_length=30,min_length=6,error_messages={"max_length":"密码最多不能超过30个字符","min_length":"密码最少不能少于6个字符"})
    remember = forms.IntegerField(required=False)

class RegisterForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11,min_length=11,validators=[validators.RegexValidator(r'1')])
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(max_length=30,min_length=6,error_messages={"max_length":"密码最多不能超过30个字符","min_length":"密码最少不能少于6个字符"})
    password2 = forms.CharField(max_length=30,min_length=6,error_messages={"max_length":"密码最多不能超过30个字符","min_length":"密码最少不能少于6个字符"})
    img_captcha = forms.CharField(max_length=4,min_length=4)
    sms_captcha = forms.CharField(max_length=4,min_length=4)

    def clean(self):
        # 所有字段都符合要求，执行此处开始验证
        cleaned_data = super(RegisterForm,self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致')

        # 验证图形验证码
        img_captcha = cleaned_data.get('img_captcha')
        cache_img_captcha = cache.get(img_captcha.lower())
        if not cache_img_captcha or img_captcha.lower() != cache_img_captcha.lower():
            raise forms.ValidationError('图形验证码输入错误')


        # 验证短信验证码
        telephone = cleaned_data.get('telephone')
        sms_captcha = cleaned_data.get('sms_captcha')
        cache_sms_captcha = cache.get(telephone)
        if not cache_sms_captcha or sms_captcha.lower()!= cache_sms_captcha:
            raise forms.ValidationError('短信验证码错误')

        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            forms.ValidationError('该手机号也被注册')
        return cleaned_data