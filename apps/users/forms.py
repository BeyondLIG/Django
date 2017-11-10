#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Chunguang Li
from captcha.fields import CaptchaField
from django import forms

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(required=True, error_messages={'invalid': '验证码错误'})


class ModifyForm(forms.Form):
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile']


