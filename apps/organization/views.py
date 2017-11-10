# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CityDict, CourseOrg, Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite


# Create your views here.


class OrgListView(View):
    def get(self, request):
        all_cities = CityDict.objects.all()
        all_courses = CourseOrg.objects.all()
        hot_orgs = all_courses.order_by('click_nums')

        keywords = request.GET.get('keywords', '')
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords))

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_courses = all_courses.filter(city_id=int(city_id))

        # 帅选类别
        category = request.GET.get('ct', '')
        if category:
            all_courses = all_courses.filter(category=category)

        # 学习人数
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('students')
                all_courses = all_courses.order_by('students')
            if sort == 'courses':
                all_courses = all_courses.order_by('course_nums')

        course_num = all_courses.count()

        # 分页
        p = Paginator(all_courses, 3, request=request)

        all_orgs = p.page(page)

        return render(request, 'org-list.html', {'all_cities': all_cities, 'all_orgs': all_orgs, 'hot_orgs': hot_orgs, 'course_num': course_num, 'city_id': city_id, 'ct': category, 'sort': sort})


class AddUserAskView(View):
    """
    添加用户咨询
    """
    def post(self, request):
        userasK_form = UserAskForm(request.POST)
        if userasK_form.is_valid():
            user_ask = userasK_form.save(commit=True) # commit=True，保存数据到数据库
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status': 'fail', 'msg': '添加出错}", content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = 'home'
        org = CourseOrg.objects.get(id=int(org_id))
        all_courses = org.course_set.all()[:3]
        all_teachers = org.teacher_set.all()[:1]
        has_fav = False
        if request.user.is_authenticated():
            exist_records = UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2)
            if exist_records:
                has_fav = True
        return render(request, 'org-detail-homepage.html', {'all_courses': all_courses, 'all_teachers': all_teachers, 'org': org, 'current_page': current_page, 'has_fav': has_fav})


class OrgCoursesView(View):
    """
    机构课程
    """
    def get(self, request, org_id):
        current_page = 'courses'
        org = CourseOrg.objects.get(id=int(org_id))
        all_courses = org.course_set.all()
        has_fav = False
        if request.user.is_authenticated():
            exist_records = UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2)
            if exist_records:
                has_fav = True
        return render(request, 'org-detail-course.html', {'all_courses': all_courses, 'org': org, 'current_page': current_page, 'has_fav': has_fav})


class OrgDescView(View):
    """
    机构介绍
    """
    def get(self, request, org_id):
        current_page = 'desc'
        org = CourseOrg.objects.get(id=int(org_id))
        # 机构点击数
        org.click_nums += 1
        org.save()

        has_fav = False
        if request.user.is_authenticated():
            exist_records = UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2)
            if exist_records:
                has_fav = True
        return render(request, 'org-detail-desc.html', {'org': org, 'current_page': current_page, 'has_fav': has_fav})


class OrgTeacherView(View):
    """
    机构教师
    """
    def get(self, request, org_id):
        current_page = 'teacher'
        org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            exist_records = UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2)
            if exist_records:
                has_fav = True
        return render(request, 'org-detail-teachers.html', {'all_teachers': all_teachers, 'org': org, 'current_page': current_page, 'has_fav': has_fav})


class AddFavView(View):
    """
    收藏，取消收藏
    """
    def post(self, request):
        # 根据fav_type判断是哪种类型的收藏
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户是否登录
        if not request.user.is_authenticated():
            return HttpResponse("{'status': 'fail', 'msg': '用户未登录}", content_type='application/json')

        # 判断是收藏或取消收藏
        if int(fav_id) > 0 and int(fav_type) > 0:
            exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
            if exist_records:
                # 取消收藏
                exist_records.delete()

                # 收藏数减1
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums -= 1
                    if course.fav_nums < 0:
                        course.fav_nums = 0
                    course.save()
                elif int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums -= 1
                    if org.fav_nums < 0:
                        org.fav_nums = 0
                    org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums -= 1
                    if teacher.fav_nums < 0:
                        teacher.fav_nums = 0
                    teacher.save()

                return HttpResponse("{'status': 'success', 'msg': '收藏}", content_type='application/json')
            else:
                # 收藏
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                # 收藏数加1
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums += 1
                    org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse("{'status': 'success', 'msg': '已收藏}", content_type='application/json')
        else:
            return HttpResponse("{'status': 'fail', 'msg': '收藏出错}", content_type='application/json')


class TeacherListView(View):
    """
    授课教师列表页
    """
    def get(self, request):
        teachers = Teacher.objects.all()
        teachers_nums = teachers.count()
        hot_teachers = teachers.order_by('-click_nums')[:3]

        keywords = request.GET.get('keywords', '')
        if keywords:
            teachers = teachers.filter(Q(name__icontains=keywords) | Q(work_company__icontains=keywords) | Q(
                work_position__icontains=keywords))

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                teachers = teachers.order_by('-click_nums')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 分页
        p = Paginator(teachers, 1, request=request)
        teachers = p.page(page)
        return render(request, 'teachers-list.html', {
            'teachers': teachers,
            'teachers_nums': teachers_nums,
            'hot_teachers': hot_teachers,
            'sort': sort
        })


class TeacherDetailView(View):
    """
    教师详情页
    """
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        # 教师点击数
        teacher.click_nums += 1
        teacher.save()

        courses = teacher.course_set.all()
        org = teacher.org
        hot_teachers = Teacher.objects.all().order_by('-click_nums')[:3]
        has_teacher_fav = False
        has_org_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_teacher_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_org_fav = True

        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'courses': courses,
            'org': org,
            'hot_teachers': hot_teachers,
            'has_teacher_fav': has_teacher_fav,
            'has_org_fav': has_org_fav
        })