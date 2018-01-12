#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/1/11 19:42
# Author: xycfree
# @Descript:


import base64
import logging
import string
import traceback
from random import Random

from django.core.mail import send_mail
from django.utils import timezone
from itsdangerous import URLSafeTimedSerializer as utsr

from py_web.settings import EMAIL_FROM, SECRET_KEY
from userinfo.models import EmailVerifyRecord

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__file__)


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    # code = random_str(16)
    code = Token().generate_validate_token(email)
    log.debug('token: {}'.format(code))
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.send_time = timezone.now()
    email_record.save()

    # http://118.89.105.65 是我自己的服务器 IP 地址，你部署的时候，请换成你自己的 IP 或 域名
    _ip = "http://127.0.0.1:8003/"

    if send_type == 'register':
        email_title = '注册激活链接'
        email_body = '请点击下面的链接激活你的账号：{}active/{}, 链接有效时间为24小时'.format(_ip, code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        log.debug('send_status: {}'.format(send_status))
        if send_status:
            log.info('发送成功')
            return True
        else:
            log.info('发送失败')
            return False

    elif send_type == 'forget':
        email_title = '密码重置链接'
        email_body = '请点击下面的链接重置你的密码：{}/reset/{}, 链接有效时间为24小'.format(_ip, code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            log.info("发送成功")
            return True
        else:
            log.info('发送失败')
            return False


def random_str(random_length=16):
    code = ''
    # 26个大小写字母加数字
    chars = string.ascii_letters + str(string.digits)
    length = len(chars) - 1

    for i in range(random_length):
        code += chars[Random().randint(0, length)]
    return code


class Token(object):
    """
        security_key就是settings.py中设置的SECRET_KEY，salt是经过base64加密的SECRET_KEY，
        generate_validate_token函数通过URLSafeTimedSerializer在用户注册时生成一个令牌。用户名在令牌中被编了码。
        生成令牌之后，会将带有token的验证链接发送到注册邮箱。在confirm_validate_token函数中，只要令牌没过期，
        那它就会返回一个用户名，过期时间为3600秒。
    """
    def __init__(self, security_key=SECRET_KEY):
        self.security_key = security_key
        self.salt = base64.b64encode(security_key.encode(encoding='utf-8'))  # 编码 注意encodestr类型是byte,不是str
        # decodestr = base64.b64decode(self.salt)  # 解码

    def generate_validate_token(self, username):
        """ generate_validate_token函数通过URLSafeTimedSerializer在用户注册时生成一个令牌。用户名在令牌中被编了码。
            生成令牌之后，会将带有token的验证链接发送到注册邮箱。
        :param username:
        :return:
        """
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)

    def confirm_validate_token(self, token, expiration=60*60*24):
        """ 在confirm_validate_token函数中，只要令牌没过期，那它就会返回一个用户名，过期时间为3600秒。
        :param token:
        :param expiration: 过期时间
        :return:
        """
        try:
            serializer = utsr(self.security_key)
            return serializer.loads(token, salt=self.salt, max_age=expiration)
        except Exception as e:
            log.error("Error: {}, {}".format(traceback.format_exc(), e))
            return None