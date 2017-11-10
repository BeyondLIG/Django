# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from organization.models import CourseOrg
from organization.models import Teacher


# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name='教师', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="课程名称")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    is_banner = models.CharField(default=False, max_length=10, verbose_name='是否轮播')
    detail = UEditorField(verbose_name=u"详情", width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default="")
    degree = models.CharField(choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="course/%Y/%m", verbose_name="封面图片", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    category = models.CharField(default='后端开发', max_length=20, verbose_name="课程类别")
    tag = models.CharField(default='', verbose_name='课程标签', max_length=20)
    youneed_known = models.CharField(default='', max_length=200, verbose_name='课程须知')
    teacher_tell = models.CharField(default='', max_length=100, verbose_name='老师告诉你')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        return self.lession_set.all().count()

    get_zj_nums.short_description = '章节数'  # 后台显示函数

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.projectsedu.com'>跳转</>")

    go_to.short_description = '跳转'

    def get_course_lession(self):
        return self.lession_set.all()

    def get_course_resource(self):
        return self.courseresource_set.all()

    def __unicode__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True  # 十分重要 True不会创建新的数据库表，否则会新建数据库表


class Lession(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lession_vedio(self):
        return self.vedio_set.all()


class Vedio(models.Model):
    lession = models.ForeignKey(Lession, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name="视频名")
    url = models.CharField(default='', max_length=200, verbose_name='视频链接')
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name="名称")
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name