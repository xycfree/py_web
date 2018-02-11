# coding: utf-8
import xadmin
from .models import Article, Category, Link


class ArticleAdmin(object):
    """后台-文章"""

    list_display = ['author', 'category', 'tags', 'title', 'article_from', 'reading_num', 'is_top', 'rank',
                    'status', 'create_time', 'update_time']  # 文章 titles
    search_fields = ['author', 'category', 'tags', 'title', 'summary', 'article_from', 'content',
                     'reading_num', 'is_top', 'rank', 'status']  # 过滤器条件
    list_filter = ['author__username', 'category__name', 'tags', 'summary', 'article_from', 'content',
                   'reading_num', 'is_top', 'rank', 'status', 'create_time', 'update_time']  # 增加文章字段
    readonly_fields = []
    style_fields = {'content': 'ueditor'}  # 正文-富文本
    relfield_style = 'fk-ajax'


class CategoryAdmin(object):
    """后台-文章类型"""
    list_display = ['name', 'rank', 'create_time', 'update_time']  # 文章类型 titles
    search_fields = ['name', 'rank']  # 查询条件
    list_filter = ['name', 'rank', 'create_time', 'update_time']  # 增加文章字段


class LinkAdmin(object):
    """后台-友情链接"""
    list_display = ['name', 'url', 'rank', 'create_time', 'update_time']  # 友情链接titles
    search_fields = ['name', 'url', 'rank']  # 查询
    list_filter = ['name', 'url', 'rank', 'create_time', 'update_time']  # 增加文章字段


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Link, LinkAdmin)
