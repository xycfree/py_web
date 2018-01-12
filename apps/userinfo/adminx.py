#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/1/11 16:13
# @Descript:


import xadmin
from xadmin import views

from .models import Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "博客后台管理"  # 设置头标题
    site_footer = "开发者在线"  # 设置脚标题
    menu_style = 'accordion'  # 主题


class BannerAdmin(object):
    """后台-轮播图"""
    list_display = ['title', 'image', 'url', 'rank', 'create_time']
    search_fields = ['title', 'image', 'url', 'rank']
    list_filter = ['title', 'image', 'url', 'rank', 'create_time']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Banner, BannerAdmin)

