#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/1/22 15:04
# Author: xycfree
# @Descript:
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from blog import views

urlpatterns = [
    # url(r'user/register', UserRegisterAPIView.as_view(), name='user_register'),
    # url(r'index/$', views.index, name='index'),
    url(r'index/$', views.Index.as_view(), name='index'),
    url(r'article/edit/$', views.ArticleEdit.as_view(), name='article_edit'),
    url(r'article/edit1/$', views.article_edit, name='article_edit'),

]

#  url('^login/$', csrf_exempt(views.LoginView.as_view())),