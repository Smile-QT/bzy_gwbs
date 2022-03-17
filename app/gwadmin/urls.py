# -*- coding: utf-8 -*-
# @Time    : 2020/9/1 15:42
# @Author  : Spring
# @FileName: urls.py
# @Software: PyCharm
from django.urls import path

from app.gwadmin.views import GwAdmin, GwUser, GwUserAnswer, GwExamTime, GwExamImport, LoginView, logout, GwShow

urlpatterns = [

    path('login', LoginView.as_view(), name="gwlogin"),
    path('logout', logout, name="gwlogout"),
    path('', GwAdmin.as_view(), name="gwadmin"),

    path('user', GwUser.as_view(), name="gwuser"),
    path('useranswer', GwUserAnswer.as_view(), name="useranswer"),
    path('examtime', GwExamTime.as_view(), name="examtime"),
    path('examimport', GwExamImport.as_view(), name="examimport"),
    path('show', GwShow.as_view(), name="gwshow"),

]
