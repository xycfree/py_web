#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/1/22 14:13
# Author: xycfree
# @Descript:

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method is permissions.SAFE_METHODS:  # 'GET', 'HEAD', 'OPTIONS'
            return True
        return request.session.get('user_id') is not None

    def has_object_permission(self, request, view, article):
        if request.method in permissions.SAFE_METHODS:
            return True
        return article.owner.id == request.session.get('user_id')
