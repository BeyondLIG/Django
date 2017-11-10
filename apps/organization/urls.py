#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Chunguang Li
from django.conf.urls import url, include
from .views import OrgListView, AddUserAskView
from .views import OrgHomeView, OrgCoursesView, OrgDescView, OrgTeacherView, AddFavView, TeacherListView, TeacherDetailView


urlpatterns = [
    url(r'^list/$', OrgListView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^courses/(?P<org_id>\d+)/$', OrgCoursesView.as_view(), name='org_courses'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),

    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),
]
