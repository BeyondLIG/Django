#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Chunguang Li
from django.conf.urls import url, include

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCoursesView, \
    MyFavCourseView, MyFavOrgView, MyFavTeacherView, MyMessageView


urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name='users_info'),

    # 上传头像
    url(r'^upload_image/$', UploadImageView.as_view(), name='upload_image'),

    # 修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),

    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),

    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    # 我的课程
    url(r'^my_courses/$', MyCoursesView.as_view(), name='my_courses'),

    # 我的收藏
    # 公开课程
    url(r'^fav/courses/$', MyFavCourseView.as_view(), name='fav_course'),

    # 我的收藏
    # 课程机构
    url(r'^fav/org/$', MyFavOrgView.as_view(), name='fav_org'),

    # 我的收藏
    # 授课教师
    url(r'^fav/teacher/$', MyFavTeacherView.as_view(), name='fav_teacher'),

    # 我的信息
    url(r'^message$', MyMessageView.as_view(), name='users_message'),
]