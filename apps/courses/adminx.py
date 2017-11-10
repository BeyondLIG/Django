#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Chunguang Li
import xadmin

from .models import Course, Lession, Vedio, CourseResource, BannerCourse


class LessionInline(object):
    model = Lession
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image',
                    'click_nums', 'add_time', 'get_zj_nums', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                   'add_time']
    # 默认的排序
    ordering = ['-click_nums']
    # 只读字段
    readonly_fields = ['click_nums', 'fav_nums']
    # 不显示的字段
    exclude = ['students']
    inlines = [LessionInline, CourseResourceInline]
    # 自动刷新时间
    refresh_times = [3, 5]
    # style_fields = {"detail": "ueditor"}

    #import_excel位True，excel导入,会覆盖插件中(plugins/excel.py)import_excel的默认值
    import_excel = True

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        return qs.filter(is_banner=False)

    def save_models(self):
        # 在保存课程时统计课程机构的课程数
        obj = self.new_obj
        obj.save()

        if obj.course_org:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

            # 将导入的excel文件内容存入数据库的course表中

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image',
                    'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                   'add_time']
    # 默认的排序
    ordering = ['-click_nums']
    # 只读字段
    readonly_fields = ['click_nums', 'fav_nums']
    # 不显示的字段
    exclude = ['students']
    inlines = [LessionInline, CourseResourceInline]

    # 过滤操作
    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        return qs.filter(is_banner=True)


class LessionAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VedioAdmin(object):
    list_display = ['lession', 'name', 'add_time']
    search_fields = ['lession', 'name']
    list_filter = ['lession__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lession, LessionAdmin)
xadmin.site.register(Vedio, VedioAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
