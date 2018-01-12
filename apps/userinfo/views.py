#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/1/11 16:13
# @Descript:
import json
import logging
import traceback

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from common.send_email import send_register_email, Token
from userinfo.models import UserProfile, EmailVerifyRecord
from common.conf import resp_code
from common.utils import validate_email, validate_pass_len, MyJSONEncoder, http_response_return
from py_web.settings import SECRET_KEY

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__file__)
token_confirm = Token(SECRET_KEY)

# 让用户可以用邮箱登录
# setting 里要有对应的配置
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            log.error("Error: {}, {}".format(traceback.format_exc(), e))
            return None


def index(request):
    # return render(request, 'index.html')
    return HttpResponse('welcome to django!')


@csrf_exempt
def login(request):
    if request.method == 'GET':
        return HttpResponse('login is get request')

    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        log.debug('用户名: {}, 密码: {}'.format(username, password))
        if username is '' or password is '':
            res = {'code': 'C00003', 'msg': resp_code.get('C00003')}
            return http_response_return(res)
        else:
            user = authenticate(username=username, password=password)
            log.debug('user: {}'.format(user))
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    request.session.set_expiry(60 * 60 * 2)  # 设置session过期时间, 默认14天
                    res = {'code': 'C00000', 'msg': resp_code.get('C00000')}
                    return http_response_return(res)
                res = {'code': 'C10001', 'msg': resp_code.get('C10001')}
                return http_response_return(res)
            res = {'code': 'C10000', 'msg': resp_code.get('C10000')}
            return http_response_return(res)
    else:
        return http_response_return('other')


@csrf_exempt
@login_required
def logout(request):
    auth_logout(request)
    return http_response_return('logout')


@csrf_exempt
def register(request):
    if request.method == 'GET':
        return http_response_return("register is get request!")
    elif request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        res = ''
        if email is '' or password is '':
            res = {'code': 'C00003', 'msg': resp_code.get('C00003')}
        elif not validate_email(email):  # 验证邮箱格式
            res = {'code': 'C10004', 'msg': resp_code.get('C10004')}
        elif not validate_pass_len(password):  # 密码长度验证
            res = {'code': 'C10005', 'msg': resp_code.get('C10005')}
        if res is not '':
            return http_response_return(res)
        if UserProfile.objects.filter(email=email):
            res = {'code': 'C10003', 'msg': resp_code.get('C10003')}
            return http_response_return(res)

        user = UserProfile.objects.create(username=email, password=password, email=email, is_active=False)
        user.set_password(password)  # make_password(password)
        user.save()

        # 注册成功,发送邮件
        try:
            send_status = send_register_email(email, send_type="register")
            log.info("邮件发送结果: {}".format(send_status))
        except Exception as e:
            log.error("Error: {}, {}".format(traceback.format_exc(), e))
        res = {'code': 'C00000', 'msg': resp_code.get('C00000')}
        return http_response_return(res)
    else:
        return http_response_return("other")


def activate(request, code):
    if request.method == 'GET':
        # 用code在数据库中过滤处信息
        # all_records = EmailVerifyRecord.objects.filter(code=code)
        # if all_records:
        #     for record in all_records:
        #         _email = record.email
        #         # 通过邮箱查找到对应的用户
        #         user = UserProfile.objects.get(email=_email)
        #         # 激活用户
        #         user.is_active = True
        #         user.save()
        #         res = {'code': 'C00000', 'msg': resp_code.get('C00000')}
        #         return http_response_return(res)
        email = ''
        try:
            email = token_confirm.confirm_validate_token(code)  # 根据token获取username
        except Exception as e:
            log.error("Error: {}, {}".format(traceback.format_exc(), e))
            log.warning("对不起, 验证码链接已经过期!")

        try:
            # 通过邮箱查找到对应的用户
            user = UserProfile.objects.get(email=email)
            # 激活用户
            user.is_active = True
            user.save()
            res = {'code': 'C00000', 'msg': resp_code.get('C00000')}
            return http_response_return(res)
        except Exception as e:
            log.error("Error: {}, {}".format(traceback.format_exc(), e))
            res = {'code': 'C10006', 'msg': resp_code.get('C10006')}
            return http_response_return(res)
    else:
        return http_response_return('post is request')




class ResetPassView(View):
    pass


class UpdateImageView(View):
    pass


class ForgetPass(View):
    pass


def forget_pwd(request):
    pass


def update_image(request):
    pass


def reset_pass(request):
    pass



