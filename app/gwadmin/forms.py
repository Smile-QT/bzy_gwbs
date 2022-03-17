# -*- coding: utf-8 -*-
# @Time    : 2020/9/2 20:25
# @Author  : Spring
# @FileName: forms.py
# @Software: PyCharm
from django import forms


class AdminUserLoginForm(forms.Form):
    name = forms.CharField(label="name", required=True, max_length=4, min_length=4)
    password = forms.CharField(label="密码", required=True, max_length=10, min_length=5)


class GwExamTimeForm(forms.Form):
    begin_time = forms.DateTimeField(label="开始时间", required=True)
    end_time = forms.DateTimeField(label="结束时间", required=True)
