# coding:utf-8

__author__ = 'xycfree'

from django.conf.urls import url, include

from userinfo import views

app_name = 'userinfo'

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^password/$', views.modify_pwd, name='password'),
    url(r'^forget/$', views.forget_pwd, name='forget_pwd'),
    url(r'^reset/$', views.reset_pwd, name='reset_pwd'),
    url(r'^center/$', views.center, name='center'),
    url(r'^user/modify/$', views.modify_user_info, name='modify_user'),


    url(r'user/image/$', views.update_image, name='updateimage'),
    url(r'^active/(?P<code>.*)/$', views.activate, name="user_active"),  # 提取出active后的所有字符赋给active_code
    url(r'^reset/(?P<code>.*)/$', views.reset_page, name="reset_page"),  # 提取出active后的所有字符赋给active_code

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

]
