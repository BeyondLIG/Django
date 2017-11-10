# _*_ encoding=utf-8 _*_
"""mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
from settings import MEDIA_ROOT
import xadmin

from users.views import user_login, LoginView, LogoutView, RegisterView, ActiveUserView, ForgetPwdView, ResetPwdView, ModifyPwdView, IndexView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),

    # url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^$', IndexView.as_view(), name='index'),

    # url(r'login/', TemplateView.as_view(template_name='login.html'), name='login'),
    # url(r'^login/$', user_login, name='login'),
    url(r'^login/$', LoginView.as_view(), name='login'),  # 查看as_view源代码
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^forgetpwd/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetPwdView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # 配置上传文件的处理函数
    url(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),

    # 生产环境下配置静态文件的处理函数
    # url(r'^static/(?P<path>.*)/$', serve, {'document_root': STATIC_ROOT}),

    # 路由分发，避免主路由过大，难以维护
    url(r'^org/', include('organization.urls', namespace='org')),
    url(r'^course/', include('courses.urls', namespace='course')),

    # 路由分发，避免主路由过大，难以维护
    url(r'^users/', include('users.urls', namespace='users')),

    # 富文本相关url
    url(r'^ueditor/', include('DjangoUeditor.urls')),
]

# 配置全局404变量
handler404 = 'users.views.page_not_found'
# 配置全局500变量
handler500 = 'users.views.page_error'