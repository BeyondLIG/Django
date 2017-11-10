#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Chunguang Li

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '幕学管理后台'
    site_footer = '慕学在线网'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    # 后台视图
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 后台搜索框
    search_fields = ['code', 'email', 'send_type']
    # 定义后台过滤搜索
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-address-card'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
