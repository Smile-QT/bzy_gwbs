# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 15:06
# @Author  : Spring
# @FileName: forms.py
# @Software: PyCharm
from django import forms


class UserLoginForm(forms.Form):
    candidate_num = forms.CharField(label="准考证号", required=True, min_length=5, max_length=20)
    password = forms.CharField(label="密码", required=True)
