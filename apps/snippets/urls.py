#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/1/17 20:00
# Author: xycfree
# @Descript:


__author__ = 'xycfree'

from django.conf.urls import url, include
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns
app_name = 'snippets'

urlpatterns = [

    # url(r'^snippets/$', views.snippet_list),
    # url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),

    url(r'^snippets/$', views.SnippetList.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),


]

urlpatterns = format_suffix_patterns(urlpatterns)  # 为我们的URLs添加可选的格式后缀

"""
    我们也可以控制响应内容的格式，通过Http中的 Accept 头(header)：
    http http://127.0.0.1:8000/snippets/ Accept:application/json  # 请求 JSON
    http http://127.0.0.1:8000/snippets/ Accept:text/html         # 请求 HTML
    
    或通过追加格式后缀（format suffix）：
    http http://127.0.0.1:8000/snippets.json  # JSON 后缀
    http http://127.0.0.1:8000/snippets.api   # 可视化 API 后缀
    
    # POST 使用表单数据
    http --form POST http://127.0.0.1:8000/snippets/ code="print 123"
    # POST 使用 JSON
    http --json POST http://127.0.0.1:8000/snippets/ code="print 456"
    
    http --json POST http://127.0.0.1:8000/register username="ICELEE" password="mypass" name="icelee"


"""