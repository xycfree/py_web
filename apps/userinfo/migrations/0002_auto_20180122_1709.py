# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-22 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='code',
            field=models.CharField(max_length=128, verbose_name='验证码'),
        ),
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='email',
            field=models.EmailField(max_length=128, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '找回密码')], max_length=64, verbose_name='验证码类型'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=36, verbose_name='手机号'),
        ),
    ]