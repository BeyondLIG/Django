#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Chunguang Li
from random import Random

from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from mxonline.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_email_verification_code(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_titel = '慕学在线网注册激活链接'
        email_body = '请点击链接激活账号：http://127.0.0.1:8000/active/{0}'.format(code)

        email_status = send_mail(email_titel, email_body, EMAIL_FROM, [email])
        if email_status:
            pass

    elif send_type == 'forget':
        email_titel = '慕学在线网重置密码链接'
        email_body = '请点击链接激活账号：http://127.0.0.1:8000/reset/{0}'.format(code)

        email_status = send_mail(email_titel, email_body, EMAIL_FROM, [email])
        if email_status:
            pass

    elif send_type == 'update_email':
        email_titel = '慕学在线网修改密码'
        email_body = '邮箱验证码：{0}'.format(code)

        email_status = send_mail(email_titel, email_body, EMAIL_FROM, [email])
        if email_status:
            pass