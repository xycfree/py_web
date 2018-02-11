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
from django.forms import model_to_dict
from django.shortcuts import render, HttpResponse
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from common.mixin_utils import LoginRequiredMixin
from common.send_email import send_register_email, Token
from userinfo.models import UserProfile, EmailVerifyRecord
from common.conf import resp_code
from common.utils import validate_email, validate_pass_len, MyJSONEncoder, http_response_return
from py_web.settings import SECRET_KEY
from userinfo.serializers import UserProfileSerializer, UserRegisterSerializer
from rest_framework import status


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
    """ 登录 """
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
    log.debug('user: {}'.format(request.user))
    auth_logout(request)
    return http_response_return('logout')


@csrf_exempt
def register(request):
    """ 用户注册 """
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
        try:
            user = UserProfile.objects.create(username=email, password=password, email=email, is_active=False)
            user.set_password(password)  # make_password(password)
            user.save()
        except Exception as e:
            log.error("Error: {}, {}".format(traceback.format_exc(), e))
            res = {'code': 'C10011', 'msg': resp_code.get('C10011')}
            return http_response_return(res)

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
    """ 用户激活 """
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


def forget_pwd(request):
    """ 忘记密码页面，发送邮件 """
    if request.method == 'POST':
        email = request.POST.get('email', '')
        if email is '':
            res = {'code': 'C00003', 'msg': resp_code.get('C00003')}
            return http_response_return(res)
        if not validate_email(email):
            res = {'code': 'C10004', 'msg': resp_code.get('C10004')}
            return http_response_return(res)
        res = send_register_email(email, send_type='forget')
        if res:
            res = {'code': 'C00000', 'msg': '邮件发送成功'}
        else:
            res = {'code': 'C10010', 'msg': resp_code.get('C10010')}
        return http_response_return(res)
    else:
        return http_response_return("forget password is get requist")


def reset_page(request, code):
    """ 用户进入到重置密码页面 """
    #  如果第二次进来，链接就失效, 该功能没有实现, 需优化
    if request.method == 'GET':
        all_records = EmailVerifyRecord.objects.filter(code=code)
        if all_records:
            for r in all_records:
                email = r.email
                res = {'code': 'C00000', 'msg': resp_code.get('C00000'), 'data': {'email': email, 'code': code}}
                return http_response_return(res)
        res = {'code': 'C10012', 'msg': resp_code.get('C10012'), 'data': {'email': ''}}
        return http_response_return(res)
    else:
        return http_response_return('reset pwd is post requist')


def reset_pwd(request):
    """ 用户重置密码 """
    if request.method == 'POST':
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        pwd = request.POST.get('new_pass', '')
        re_pwd = request.POST.get('res_pass', '')
        if email is '' or pwd is '' or re_pwd is '' or code is '':
            res = {'code': 'C00003', 'msg': resp_code.get('C00003')}
            return http_response_return(res)
        try:
            _email = EmailVerifyRecord.objects.get(code=code).__dict__.get('email', '')
            if email != _email:
                res = {'code': 'C10014', 'msg': resp_code.get('C10014')}
                return http_response_return(res)
        except Exception as e:
            log.error("Error: {}, {}".format(traceback.format_exc(), e))
            res = {'code': 'C10013', 'msg': resp_code.get('C10013')}
            return http_response_return(res)

        if not validate_pass_len(pwd):
            res = {'code': 'C10005', 'msg': resp_code.get('C10005')}
        elif pwd != re_pwd:
            res = {'code': 'C10008', 'msg': resp_code.get('C10008')}
        else:
            try:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pwd)
                user.save()
                res = {'code': 'C00000', 'msg': resp_code.get('C00000')}
            except Exception as e:
                log.error("Error: {}, {}".format(traceback.format_exc(), e))
                res = {'code': 'C10009', 'msg': resp_code.get('C10009')}
        return http_response_return(res)


@csrf_exempt
@login_required
def modify_pwd(request):
    """ 用户修改密码 """
    print(request.user)
    if request.method == 'POST':
        user = request.user
        old_pass = request.POST.get('old_pass', '')
        new_pass = request.POST.get('new_pass', '')
        res_pass = request.POST.get('res_pass', '')
        log.debug("pass: {}, new_pass: {}, res_pass: {}".format(old_pass, new_pass, res_pass))
        if old_pass is '' or new_pass is '' or res_pass is '':
            res = {'code': 'C00003', 'msg': resp_code.get('C00003')}
            return http_response_return(res)
        if not user.check_password(old_pass):
            res = {'code': 'C10007', 'msg': resp_code.get('C10007')}
        elif not validate_pass_len(new_pass):
            res = {'code': 'C10005', 'msg': resp_code.get('C10005')}
        elif not new_pass == res_pass:
            res = {'code': 'C10008', 'msg': resp_code.get('C10008')}
        else:
            try:
                user.set_password(new_pass)
                user.save()
                res = {'code': 'C00000', 'msg': '密码修改成功'}
            except Exception as e:
                log.error('Error: {}, {}'.format(traceback.format_exc(), e))
                res = {'code': 'C10009', 'msg': resp_code.get('C10009')}
        return http_response_return(res)

    else:
        http_response_return('reset password is get requist!')


@csrf_exempt
@login_required
def center(request):
    """个人中心 """

    if request.method == 'GET':

        user = request.user
        try:
            users = UserProfile.objects.get(username=user)
            log.debug('user info: {}'.format(users.__dict__))
            data = {'username': users.__dict__.get('username', ''), 'email': users.__dict__.get('email', ''),
                    'address': users.__dict__.get('address', ''), 'nickname': users.__dict__.get('nickname', ''),
                    'phone': users.__dict__.get('phone', '')}
            res = {'code': 'C00000', 'msg': resp_code.get('C00000'), 'data': data}  # users.__dict__
        except Exception as e:
            log.error("Error: {}, {}".format(traceback.format_exc(), e))
            res = {'code': 'C00002', 'msg': resp_code.get('C00002'), 'data': {}}
        return http_response_return(res)
    else:
        return http_response_return("center is post requist")


@csrf_exempt
@login_required
def modify_user_info(request):
    """ 用户信息修改 """

    if request.method == 'POST':
        try:
            _di = dict(request.POST.items())  # query_set to dict
            log.debug('_di: {}'.format(_di))
            UserProfile.objects.filter(username=request.user).update(**_di)  # 字典更新, 不需要save
            res = {'code': 'C00000', 'msg': resp_code.get('C00000')}
        except Exception as e:
            log.error("Error: {}, {}".format(traceback.format_exc(), e))
            res = {'code': 'C00001', 'msg': resp_code.get('C00001')}
        return http_response_return(res)
    else:
        return http_response_return("modify user info is get requist")


@csrf_exempt
@login_required
def update_image(request):
    """ 更新头像 """
    if request.method == 'POST':
        image = request.POST.get('image', '')
        if image is '':
            res = {'code': 'C00003', 'msg': resp_code.get('C00003')}
            return http_response_return(res)
        try:
            user = UserProfile.objects.get(username=request.user)
            user.image = image
            user.save()
            res = {'code': 'C00000', 'msg': '头像修改成功'}
        except Exception as e:
            log.error("Error: {}, {}".format(traceback.format_exc(), e))
            res = {'code': 'C00001', 'msg': '头像修改失败'}
        return http_response_return(res)

    else:
        return http_response_return('modify image is get requist')


class UserInfoView(LoginRequiredMixin, View):
    pass


# 用户
class UserList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer