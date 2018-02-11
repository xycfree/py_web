#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/1/19 17:02
# Author: xycfree
# @Descript:
from rest_framework import serializers

from blog.models import Article
from userinfo.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    # blog_set = serializers.PrimaryKeyRelatedField(many=True, queryset=Article.objects.all())

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'nickname', 'email', 'phone', 'address')  # get请求显示的字段


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email')
