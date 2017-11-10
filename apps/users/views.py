# _*_ encoding:utf-8 _*_
import json
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyForm, UploadImageForm, UserInfoForm
from utils.email_send import send_email_verification_code
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from courses.models import Course
from organization.models import CourseOrg, Teacher

# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(username=username, password=password)  # django\contrib\auth\backends.py
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {'msg': '用户名或密码错误'})
    elif request.method == 'GET':
        return render(request, 'login.html')


# django url映射更适合应用view类
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
        pass

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        # django重定向
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '').strip()  # 3587861981
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在'})

            password = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.password = make_password(password)
            user_profile.save()

            send_email_verification_code(email, 'register')

            # 生成用户注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册'
            user_message.save()

            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user_profile = UserProfile.objects.get(email=email)
                user_profile.is_active = True
                user_profile.save()

                return render(request, 'login.html')
        else:
            return render(request, 'active_fail.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                send_email_verification_code(email, send_type='forget')
                return render(request, 'send_success.html')
            else:
                return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'msg': '用户不存在'})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetPwdView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            email = request.POST.get('email', '')
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'msg': '两次密码不一致', 'email': email, 'modify_form': modify_form})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        else:
            return render(request, 'password_reset.html', {'modify_form': modify_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    个人信息页
    """
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        userinfo_form = UserInfoForm(request.POST, instance=request.user)
        if userinfo_form.is_valid():
            userinfo_form.save()
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse(json.dumps(userinfo_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status': 'fail'}", content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
    """
    个人中心修改密码
    """
    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse("{'status': 'fail', 'msg': '密码不一致'}", content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse("{'email': '邮箱已存在'}", content_type='application/json')

        send_email_verification_code(email, 'update_email')
        return HttpResponse("{'status': 'success'}", content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改邮箱
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        if EmailVerifyRecord.objects.filter(email=email, send_type='update_email', code=code):
            request.user.email = email
            request.user.save()
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse("{'email': '验证码出错'}", content_type='application/json')


class MyCoursesView(LoginRequiredMixin, View):
    """
    我的课程
    """
    def get(self, request):
        user = request.user
        user_courses = UserCourse.objects.filter(user_id=user.id)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    我的收藏：公开课
    """
    def get(self, request):
        user = request.user
        user_favs = UserFavorite.objects.filter(user_id=user.id, fav_type=1)
        fav_ids = [user_fav.fav_id for user_fav in user_favs]
        fav_courses = Course.objects.filter(id__in=fav_ids)

        return render(request, 'usercenter-fav-course.html', {
            'fav_courses': fav_courses
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """
    我的收藏：课程机构
    """
    def get(self, request):
        user = request.user
        user_favs = UserFavorite.objects.filter(user_id=user.id, fav_type=1)
        fav_ids = [user_fav.fav_id for user_fav in user_favs]
        fav_orgs = CourseOrg.objects.filter(id__in=fav_ids)

        return render(request, 'usercenter-fav-org.html', {
            'fav_orgs': fav_orgs
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    我的收藏：授课教师
    """
    def get(self, request):
        user = request.user
        user_favs = UserFavorite.objects.filter(user_id=user.id, fav_type=3)
        fav_ids = [user_fav.fav_id for user_fav in user_favs]
        fav_teachers = Teacher.objects.filter(id__in=fav_ids)

        return render(request, 'usercenter-fav-teacher.html', {
            'fav_teachers': fav_teachers
        })


class MyMessageView(LoginRequiredMixin, View):
    """我的信息页"""
    def get(self, request):
        user = request.user
        user_messages = UserMessage.objects.filter(user=user.id)

        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for message in all_unread_messages:
            message.has_read = True
            message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 分页
        p = Paginator(user_messages, 3, request=request)

        user_messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'user_messages': user_messages
        })


class IndexView(View):
    """
    首页
    """
    def get(self, request):
        # 轮播图
        banners = Banner.objects.all().order_by('index')
        # 课程
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:2]
        # 机构
        orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'banners': banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'orgs': orgs
        })


def page_not_found(request):
    """
    配置404页面函数
    """
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    """
    配置500页面函数
    """
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response