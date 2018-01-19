#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/1/19 17:02
# Author: xycfree
# @Descript:
from rest_framework import serializers

from userinfo.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    # userinfo = serializers.PrimaryKeyRelatedField(many=True, queryset=UserProfile.objects.all())

    class Meta:
        model = UserProfile
        fields = ('id','username', 'email', 'profile', 'address', 'phone', 'nickname', 'image', 'au',
                  'topic_num', 'visit_num', 'comment_num', 'create_time', 'update_time')