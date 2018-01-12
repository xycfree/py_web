#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/1/11 17:54
# Author: xycfree
# @Descript:
import datetime
import decimal
import json
import logging
import traceback

from django.http import HttpResponse

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__file__)


class MyJSONEncoder(json.JSONEncoder):
    """str转换json时对时间格式化"""
    def default(self, obj):
        if isinstance(obj, (datetime.datetime,)):
            return str(obj.strftime("%Y-%m-%d %H:%M:%S"))
        elif isinstance(obj, (decimal.Decimal,)):
            return str(obj)
        elif isinstance(obj, (datetime.date,)):
            return str(obj.strftime("%Y-%m-%d"))
        else:
            return super().default(obj)


def validate_email(email):
    """ 验证邮箱是否有效
    :param email:
    :return:
    """
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def validate_pass_len(password, min=8, max=32):
    """ 验证密码长度
    :param length:
    :param password: 默认最小8位
    :return:
    """
    try:
        if min <= len(password) <= max:
            return True
        else:
            return False
    except Exception as e:
        log.error("Error: {}, {}".format(traceback.format_exc(), e))
        return False


def http_response_return(res, **kwargs):
    """ views HttpResponse 返回方法
    :param res: 返回数据，字典/字符
    :param kwargs:
    :return:
    """
    log.debug("返回信息: {}".format(res))
    res = HttpResponse(json.dumps(res, ensure_ascii=False, cls=MyJSONEncoder),
                       content_type="application/json;charset=utf-8")
    return res