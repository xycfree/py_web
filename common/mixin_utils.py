#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/1/16 19:09
# Author: xycfree
# @Descript:
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from py_web.settings import LOGIN_URL


class LoginRequiredMixin(object):
    """ 认证装饰器 """
    @method_decorator(login_required(login_url=LOGIN_URL))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)