#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/1/22 13:49
# Author: xycfree
# @Descript:

from rest_framework import serializers
from blog.models import Category, Article, Link


class ArticleSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='author.nickname')  # 只读

    class Meta:
        model = Article
        fields = ('id', 'author', 'title', 'summary', 'tags', 'content', 'reading_num', 'article_from')



