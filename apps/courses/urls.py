#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Chunguang Li
from django.conf.urls import url, include

from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, VedioPlayView


urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^info/(?P<course_id>\d+)$', CourseInfoView.as_view(), name='course_info'),
    url(r'^comment/(?P<course_id>\d+)$', CourseCommentView.as_view(), name='course_comment'),
    url(r'^vedio/(?P<vedio_id>\d+)$', VedioPlayView.as_view(), name='vedio_play'),
]
