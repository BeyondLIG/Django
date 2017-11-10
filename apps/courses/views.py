# _*_ encoding=utf-8 _*_
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Course, Vedio
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CourseListView(View):
    """
    课程列表页
    """
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        keywords = request.GET.get('keywords', '')
        if keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(detail__icontains=keywords))

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
            if sort == 'students':
                all_courses = all_courses.order_by('-students')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 分页
        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses
        })


class CourseDetailView(View):
    '''
    课程详情页
    '''

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_nums += 1
        course.save()

        tag = course.tag
        if tag:
            related_courses = Course.objects.filter(tag=tag)
        else:
            related_courses = []

        user_courses = course.usercourse_set.all()

        has_fav_course = False
        has_fav_org = False

        # 判断用户是否登录
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.id), fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.id), fav_type=2):
                has_fav_org = True

        return render(request, 'course-detail.html', {
            'course': course,
            'user_courses': user_courses,
            'related_courses': related_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程视频信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 课程学习人数
        course.students += 1
        course.save()

        # 取出学习过该课程的用户还学习过什么课程
        user_courses = UserCourse.objects.filter(course=course)
        # 取出用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出课程
        course_ids = [user_course.course.id for user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids)
        return render(request, 'course-video.html', {
            'course': course,
            'related_courses': related_courses
        })


class CourseCommentView(LoginRequiredMixin, View):
    """
    课程评论信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        comments = course.coursecomments_set.all()
        # 取出学习过该课程的用户还学习过什么课程
        user_courses = UserCourse.objects.filter(course=course)
        # 取出用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出课程
        course_ids = [user_course.course.id for user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids)
        return render(request, 'course-comment.html', {
            'course': course,
            'comments': comments,
            'related_courses': related_courses
        })


class VedioPlayView(View):
    """
    视频播放页
    """
    def get(self, request, vedio_id):
        vedio = Vedio.objects.get(id=int(vedio_id))
        course = vedio.lession
        # 取出学习过该课程的用户还学习过什么课程
        user_courses = UserCourse.objects.filter(course=course)
        # 取出用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出课程
        course_ids = [user_course.course.id for user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids)
        return render(request, 'course-play.html', {
            'vedio': vedio,
            'course': course,
            'related_courses': related_courses
        })











