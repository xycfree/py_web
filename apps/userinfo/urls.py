# coding:utf-8

__author__ = 'xycfree'

from django.conf.urls import url, include

from userinfo import views as userinfo_views

app_name = 'userinfo'

urlpatterns = [

    url(r'^$', userinfo_views.index, name='index'),
    url(r'^login/$', userinfo_views.login, name='login'),
    url(r'^logout/$', userinfo_views.logout, name='logout'),
    url(r'^register/$', userinfo_views.register, name='register'),
    url(r'^password/$', userinfo_views.modify_pwd, name='password'),
    url(r'^forget/$', userinfo_views.forget_pwd, name='forget_pwd'),
    url(r'^reset/$', userinfo_views.reset_pwd, name='reset_pwd'),
    url(r'^center/$', userinfo_views.center, name='center'),
    url(r'^user/modify/$', userinfo_views.modify_user_info, name='modify_user'),


    url(r'user/image/$', userinfo_views.update_image, name='updateimage'),
    url(r'^active/(?P<code>.*)/$', userinfo_views.activate, name="user_active"),  # 提取出active后的所有字符赋给active_code
    url(r'^reset/(?P<code>.*)/$', userinfo_views.reset_page, name="reset_page"),  # 提取出active后的所有字符赋给active_code


]
